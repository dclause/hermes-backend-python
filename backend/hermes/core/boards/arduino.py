"""
Represents a connexion to an electronic board (arduino-like) by embedding its pyserial connexion.
"""

import threading
from enum import IntEnum, Enum

from func_timeout import FunctionTimedOut, func_set_timeout

from hermes.core import logger
from hermes.core.boards import AbstractBoard, BoardException
from hermes.core.commands.blink import CommandCode
from hermes.core.devices import tag
from hermes.core.protocols import AbstractProtocol, ProtocolException
from hermes.core.protocols.usbserial import SerialProtocol, CommandListenerThread


class StringEnum(str, Enum):
    """ Enum where members are also (and must be) strings. """


# @todo should be removed ?
class ArduinoBoardType(StringEnum):
    """ Defines the arduino board types. """
    NANO = 'NANO'
    UNO = 'UNO'
    MEGA = 'MEGA'


@tag('!ARDUINO')
class ArduinoBoard(AbstractBoard):
    """ ArduinoBoard implementation """

    def __init__(self, name, serial_port: str):
        super().__init__(name)
        self._is_connected: bool = True
        self.port = serial_port
        self._connexion: AbstractProtocol = SerialProtocol(self.port)
        # Event to notify threads that they should terminate
        self._exit_event = threading.Event()
        # Number of messages we can send to the Arduino without receiving an acknowledgment
        n_messages_allowed = 3
        self._n_received_semaphore = threading.Semaphore(n_messages_allowed)
        # Lock for accessing serial file (to avoid reading and writing at the same time)
        serial_lock = threading.Lock()
        # Threads for arduino communication
        self._threads = [
            CommandListenerThread(self._connexion, self._exit_event, self._n_received_semaphore, serial_lock)]

    def open(self) -> bool:
        # ###
        # Open serial port (for communication with Arduino)
        try:
            self._connexion.open()
        except ProtocolException:
            logger.error('Board %s: Connexion could not be opened.', self.name)
            return self.close()

        # ###
        # Run the Handshake process.
        try:
            logger.info('Board %s - Try handshake', self.name)
            # if not self.handshake():
            #     raise BoardException('Handshake sequence incorrect.')
        except (FunctionTimedOut, BoardException) as error:
            logger.error('Board %s - Handshake error: %s', self.name, error)
            return self.close()

        # ###
        # Starts the send/receive threads.
        for thread in self._threads:
            thread.start()

        logger.info('Board %s - CONNECTED', self.name)
        self._is_connected = True
        return self._is_connected

    def close(self) -> bool:
        logger.info('Board %s - Close connexion', self.name)
        self._connexion.close()
        # Ends the multithreading.
        self._exit_event.set()
        self._n_received_semaphore.release()
        for thread in self._threads:
            if thread.is_alive():
                thread.join()
        self._is_connected = False
        return self._is_connected

    @func_set_timeout(1)
    def handshake(self) -> bool:
        self._connexion.send_command(CommandCode.HANDSHAKE)
        code = self._connexion.read_command()
        logger.info('Handshake received code: %s', code)
        return code == CommandCode.CONNECTED

    def send_command(self, command_code: CommandCode, *args, **kwargs):
        self._connexion.send_command(command_code, *args, **kwargs)
