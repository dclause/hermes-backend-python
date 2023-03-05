"""
Boards package.

This package contains all implemented boards provided by default in HERMES.

A board is a physical electronic circuit equipped with a programmable controller and capable to communicate with this
server via a `protocol`. (ex: Arduino boards)

Boards can be created from configs file leaving in the config/boards.yml file. Each board must validate the
schema provided within this package.
Boards are detected when the package is imported for the first time and globally available via the settings under
the `boards` key.

@see `Protocol` in the protocol package.
"""

import threading
import time
from queue import Empty
from typing import Any

from func_timeout import FunctionTimedOut, func_set_timeout
from nicegui import background_tasks

from hermes import gui
from hermes.commands import CommandFactory
from hermes.core import api, logger
from hermes.core.dictionary import MessageCode
from hermes.core.helpers import HermesException
from hermes.core.plugins import AbstractPlugin, TypeAbstractPlugin
from hermes.core.struct import ClearableQueue, MetaPluginType
from hermes.devices import AbstractDevice
from hermes.protocols import AbstractProtocol, ProtocolException


class BoardException(HermesException):
    """ Base class for board related exceptions. """


class AbstractBoard(AbstractPlugin, metaclass=MetaPluginType):
    """
    Handles the serial communication with an external board.

    The properties of a boards are :
    *id*            the board ID
    *name*          the board name
    *controller*    the board controller type (ie the class name of the board plugin type instance)
    *protocol*      the board protocol used for communication
        (@see AbstractProtocol in hermes.protocols for sub-properties)
    *actions*       a list of actuators devices (brings action to the board - led, servo, etc.)
        (@see AbstractDevice in hermes.devices for sub-properties)
    *inputs*        a list of sensors devices (outputs data from the board - PIR, button, etc.)
        (@see AbstractDevice in hermes.devices for sub-properties)

    ...
    any other properties brought by a board type plugin.
    (@see ArduinoBoard for example)
    """

    def __init__(self, protocol: AbstractProtocol):
        super().__init__()
        self.actions: dict[int, AbstractDevice] = {}
        self.inputs: dict[int, AbstractDevice] = {}

        self.connected: bool = False
        self.protocol: AbstractProtocol = protocol

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
                self.protocol,
                self._command_queue,
                self._exit_event,
                self._n_received_semaphore,
                serial_lock,
            ),
            SerialListenerThread(
                self.protocol,
                self._exit_event,
                self._n_received_semaphore,
                serial_lock,
            ),
        ]

    def open(self) -> bool:
        """
        Open the connexion from board to backend using the internal protocol.

        :return bool:
        :raise ProtocolException: Raised if the connexion could not be opened.
        """
        # ###
        # Open serial port (for communication with Arduino)
        try:
            self.protocol.open()
        except ProtocolException:
            logger.error(f'Board {self.name}: Connexion could not be opened.')
            return not self.close()

        # Wait to give time for the arduino to receive the message and open connection properly.
        # The 2sec here is obtained by trial and error using various cards. As expected, the NANO
        # is the one requiring the more wait time, hence those arbitrary 2 seconds.
        time.sleep(2)

        # ###
        # Run the Handshake process.
        try:
            logger.debug(f'Board {self.name} - Try handshake')
            self.handshake()
        except FunctionTimedOut as error:
            logger.error(f'Board {self.name} - Handshake error: {error}')
            return not self.close()

        # ###
        # Starts the send/receive threads.
        for thread in self._threads:
            thread.start()

        self.connected = True
        logger.info(f' > Board {self.name} - CONNECTED')
        return self.connected

    @classmethod
    def from_yaml(cls, constructor, node) -> TypeAbstractPlugin:
        board = super().from_yaml(constructor, node)
        board.actions = {actionPlugin.id: actionPlugin for actionPlugin in board.actions}
        board.inputs = {inputPlugin.id: inputPlugin for inputPlugin in board.inputs}
        return board

    def close(self) -> bool:
        """ Close the connexion. """
        self.protocol.close()

        # Ends the multithreading.
        self._exit_event.set()
        self._n_received_semaphore.release()
        for thread in self._threads:
            if thread.is_alive():
                thread.join()

        self.connected = False
        logger.info(f' > Board {self.name} - DISCONNECTED')
        return not self.connected

    @func_set_timeout(5)
    def handshake(self) -> None:
        """ Perform handshake between the board and the application. """

        # Handshake: send all devices to board via PATCH.
        logger.debug(f'Handshake for board `{self.name}`.')

        # Actions and Inputs are both devices and needs to be transmitted to the board,
        # so it learns about its possibilities.
        devices: dict[int, AbstractDevice] = self.actions.copy()
        devices.update(self.inputs)

        # NOTE: We cannot use the standard way to send command via the command send() method here.
        # because that one uses the self._command_queue (via SerialSenderThread) which yet started at this state.
        self.protocol.send(bytearray([MessageCode.HANDSHAKE, len(devices)]))

        # Send all commands the device can do.
        for (_, device) in devices.items():
            data: bytearray = device.as_playload()
            data = bytearray([MessageCode.PATCH]) + data
            logger.debug(f"Handshake PATCH: {data} - {list(data)}")
            self.protocol.send(data)

        # Blocking wait ACK.
        command_code = None
        while command_code is not MessageCode.ACK:
            try:
                command_code = MessageCode(self.protocol.read_byte())
                command = CommandFactory().get_by_code(command_code)
                command.receive(self.protocol)
                command.process()
            except HermesException:
                continue

    def send(self, data: bytearray):
        """
        Send the given data (via the internal protocol).

        :param bytearray data: An array of byte to transfer.
        """
        self._command_queue.put(data)

    @func_set_timeout(5)
    def gui_mutator(self, device_id: int, state: Any):
        """
        GUI Helper:  For board's devices to mutate their state via UI inputs.

        @see hermes.gui.pages.BoardPage.

        :param device_id: device ID
        :param state: new state value.
        """
        background_tasks.create(api.action(gui.CLIENT_ID, self.id, device_id, state))


_RATE = 0


# @todo move threads out of the board in the protocol.
class SerialSenderThread(threading.Thread):
    """
    Thread that send orders to the arduino.

    Note: it blocks if there is no more send_token left (here it is the n_received_semaphore).

    :param protocol: (Serial object)
    :param command_queue: (Queue)
    :param exit_event: (Threading.Event object)
    :param n_received_semaphore: (threading.Semaphore)
    :param serial_lock: (threading.Lock).
    """

    def __init__(
            self,
            protocol: AbstractProtocol,
            command_queue: ClearableQueue,
            exit_event: threading.Event,
            n_received_semaphore: threading.Semaphore,
            serial_lock: threading.Lock,
    ):
        threading.Thread.__init__(self)
        self.deamon = True
        self.protocol = protocol
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
                # @todo should be close connexion on the board if this fails ?
                self.protocol.send(data)

            time.sleep(_RATE)
        logger.debug("SerialSenderThread: thread stops.")


class SerialListenerThread(threading.Thread):
    """
    Thread that listens to communication protocol for commands and executes it.

    The thread reads a MessageCode from the communication protocol, turns it to an actual command and processes it.
    If the MessageCode is an ACK, the thread releases one lock to the n_received_semaphore semaphore to clear the way
    for the CommandSenderThread.

    Args:
    ----
        protocol (AbstractProtocol)
        exit_event (threading.Event object)
        n_received_semaphore (threading.Semaphore)
        serial_lock (threading.Lock)
    """

    def __init__(
            self,
            protocol: AbstractProtocol,
            exit_event: threading.Event,
            n_received_semaphore: threading.Semaphore,
            serial_lock: threading.Lock,
    ):
        threading.Thread.__init__(self)
        self.deamon = True
        self.protocol = protocol
        self.exit_event = exit_event
        self.n_received_semaphore = n_received_semaphore
        self.serial_lock = serial_lock

    def run(self):
        logger.debug("SerialListenerThread: thread started.")

        while not self.exit_event.is_set():
            try:
                command_code: MessageCode = MessageCode(self.protocol.read_byte())
                logger.debug(f'SerialListenerThread: receive command code {command_code}')
            except HermesException:
                time.sleep(_RATE)
                continue

            with self.serial_lock:
                command = CommandFactory().get_by_code(command_code)
                logger.debug(command)
                command.receive(self.protocol)
                command.process()

                if command_code == MessageCode.ACK:
                    self.n_received_semaphore.release()
            time.sleep(_RATE)
        logger.debug("SerialListenerThread: thread stops.")


__ALL__ = ['BoardException', 'AbstractBoard']
