"""
Boards package.
This package contains all implemented boards provided by default in HERMES.

A board is a physical electronic circuit equipped with a programmable controller and capable to communicate with this
server via a `protocol`. (ex: Arduino boards)

Boards can be created from configs file leaving in the config/boards.yml file. Each board must validate the
schema provided within this package.
Boards are detected when the package is imported for the first time and globally available via the CONFIG under
the `boards` key.

@see `Protocol` in the protocol package.
"""
import threading
import time
from queue import Empty

from func_timeout import func_set_timeout, FunctionTimedOut

from hermes.core import logger, config
from hermes.core.commands import CommandCode, CommandFactory
from hermes.core.plugins import AbstractPlugin
from hermes.core.protocols import AbstractProtocol, ProtocolException
from hermes.core.struct import MetaPluginType, ClearableQueue


class BoardException(Exception):
    """ Base class for board related exceptions. """


class AbstractBoard(AbstractPlugin, metaclass=MetaPluginType):
    """ Handles the serial communication with an external board. """

    def __init__(self, name, connexion: AbstractProtocol):
        super().__init__(name)
        self.connected: bool = False
        self._connexion: AbstractProtocol = connexion

        # Create Command queue for sending orders
        self._command_queue = ClearableQueue(4)
        # Event to notify threads that they should terminate
        self._exit_event = threading.Event()
        # Number of messages we can send to the board without receiving an acknowledgment
        self._n_received_semaphore = threading.Semaphore(5)
        # Lock for accessing serial file (to avoid reading and writing at the same time)
        serial_lock = threading.Lock()
        # Threads for arduino communication
        self._threads = [
            SerialSenderThread(
                self._connexion,
                self._command_queue,
                self._exit_event,
                self._n_received_semaphore,
                serial_lock
            ),
            SerialListenerThread(
                self._connexion,
                self._exit_event,
                self._n_received_semaphore,
                serial_lock
            )
        ]

    def open(self) -> bool:
        """
        Tries to open serial port with Arduino given the current Serial configuration.
        If not port is specified, it will be automatically detected

        Returns:
            bool

        Raises:
            SerialException: Raised if the given serial_port does not exist or cannot be opened
        """
        # ###
        # Open serial port (for communication with Arduino)
        try:
            self._connexion.open()
        except ProtocolException:
            logger.error(f'Board {self.name}: Connexion could not be opened.')
            return self.close()

        time.sleep(1)

        # ###
        # Run the Handshake process.
        try:
            logger.debug(f'Board {self.name} - Try handshake', )
            self.handshake()
        except FunctionTimedOut as error:
            logger.error(f'Board {self.name} - Handshake error: {error}')
            return self.close()

        # ###
        # Starts the send/receive threads.
        for thread in self._threads:
            thread.start()

        self.connected = True
        logger.info(f' > Board {self.name} - CONNECTED', )
        return self.connected

    def close(self) -> bool:
        """ Closes the connexion. """
        self._connexion.close()

        # Ends the multithreading.
        self._exit_event.set()
        self._n_received_semaphore.release()
        for thread in self._threads:
            if thread.is_alive():
                thread.join()

        self.connected = False
        logger.info(f' > Board {self.name} - DISCONNECTED', )
        return not self.connected

    @func_set_timeout(20)
    def handshake(self) -> None:
        """ Performs handshake between the board and the application. """

        # Handshake: send all devices to board via PATCH.
        logger.debug(f'Handshake for board `{self.name}`.')
        self._connexion.send(bytearray([CommandCode.HANDSHAKE]))
        for (_, device) in config.DEVICES.items():
            if device.board is self.id:
                data = bytearray([CommandCode.PATCH, device.code, device.id]) + \
                       device.to_bytes() + \
                       bytearray([CommandCode.END_OF_LINE])
                logger.info(f"Handshake PATCH: {data}")
                self._connexion.send(data)

        # Blocking wait ACK.
        #  @todo move this to a standardized 'wait_for_ack()' on protocol.
        command_code = None
        while command_code is not CommandCode.ACK:
            try:
                command_code = CommandCode(self._connexion.read_byte())
                command = CommandFactory().get_by_code(command_code)
                command.receive(self._connexion)
                command.process()
            except Exception:
                continue

        # # Patch all devices.
        # for (_, device) in config.DEVICES.items():
        #     if device.board is self.id:
        #         data = bytearray([CommandCode.PATCH, device.code]) + device.to_bytes
        #         self._connexion.send(data)
        #
        # # Blocking wait ACK.
        # command_code = None
        # while command_code is not CommandCode.ACK:
        #     command_code = CommandCode(self._connexion.read_byte())

    def send(self, data: bytearray):
        """
        Sends the given data (via the internal protocol)

        Args:
            data (bytearray) An array of byte to transfer.
        """
        self._command_queue.put(data)

    def __del__(self):
        logger.info(f' > Close board {self.id}')
        self.close()


_RATE = 0


# _RATE = 1 / 2000


class SerialSenderThread(threading.Thread):
    """
    Thread that send orders to the arduino
    it blocks if there is no more send_token left (here it is the n_received_semaphore).
    :param connexion: (Serial object)
    :param command_queue: (Queue)
    :param exit_event: (Threading.Event object)
    :param n_received_semaphore: (threading.Semaphore)
    :param serial_lock: (threading.Lock)
    """

    def __init__(
            self,
            connexion: AbstractProtocol,
            command_queue: ClearableQueue,
            exit_event: threading.Event,
            n_received_semaphore: threading.Semaphore,
            serial_lock: threading.Lock
    ):
        threading.Thread.__init__(self)
        self.deamon = True
        self.connexion = connexion
        self.command_queue = command_queue
        self.exit_event = exit_event
        self.n_received_semaphore = n_received_semaphore
        self.serial_lock = serial_lock

    def run(self):
        while not self.exit_event.is_set():
            self.n_received_semaphore.acquire()

            if self.exit_event.is_set():
                break

            try:
                data = self.command_queue.get_nowait()
            except Empty:
                time.sleep(_RATE)
                self.n_received_semaphore.release()
                continue

            with self.serial_lock:
                self.connexion.send(data)

            time.sleep(_RATE)
        logger.debug("SerialSenderThread: thread stops.")


class SerialListenerThread(threading.Thread):
    """
    Thread that listens to communication protocol for commands and executes it.

    The thread reads a CommandCode from the communication protocol, turns it to an actual command and processes it.
    If the CommandCode is an ACK, the thread releases one lock to the n_received_semaphore semaphore to clear the way
    for the CommandSenderThread.

    Args:
        connexion (AbstractProtocol)
        exit_event (threading.Event object)
        n_received_semaphore (threading.Semaphore)
        serial_lock (threading.Lock)
    """

    def __init__(
            self,
            connexion: AbstractProtocol,
            exit_event: threading.Event,
            n_received_semaphore: threading.Semaphore,
            serial_lock: threading.Lock
    ):
        threading.Thread.__init__(self)
        self.deamon = True
        self._connexion = connexion
        self.exit_event = exit_event
        self.n_received_semaphore = n_received_semaphore
        self.serial_lock = serial_lock

    def run(self):
        logger.debug("SerialListenerThread: thread started.")

        while not self.exit_event.is_set():
            try:
                command_code: CommandCode = CommandCode(self._connexion.read_byte())
                logger.debug(f'SerialListenerThread: receive command code {command_code}')
            except Exception:
                time.sleep(_RATE)
                continue

            with self.serial_lock:
                command = CommandFactory().get_by_code(command_code)
                logger.debug(command)
                command.receive(self._connexion)
                command.process()

                if command_code == CommandCode.ACK:
                    self.n_received_semaphore.release()
            time.sleep(_RATE)
        logger.debug("SerialListenerThread: thread stops.")


__all__ = ["AbstractBoard", "BoardException"]
