""" Core/Boards package

Contains anything related to configurable boards.
Currently, only arduino boards are supported.

Boards can be created from configs file leaving in the config/boards directory. Each board YAML file must validate the
schema provided within this package.
Boards are detected when the package is imported for the first time and globally available by import.

Examples:
    `from hermes.core.boards import BOARDS`

"""
import itertools
import threading
from abc import ABCMeta

from func_timeout import FunctionTimedOut, func_set_timeout

from hermes.core import logger
from hermes.core.command.blink import CommandCode
from hermes.core.protocols import AbstractProtocol, ProtocolException
from hermes.core.protocols.usbserial import SerialProtocol, CommandListenerThread


class BoardException(Exception):
    """ Base class for board related exceptions. """


class AbstractBoard(metaclass=ABCMeta):
    """ Handles the serial communication with an external board. """

    id_iter = itertools.count()

    # pylint: disable-next=too-many-arguments
    def __init__(self, name, serial_port: str):
        self.id = next(self.id_iter)
        self.name: str = name
        self._is_connected: bool = True
        self._connexion: AbstractProtocol = SerialProtocol(serial_port)
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
        """ Closes the connexion. """
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
        """ Performs handshake between the board and the application. """
        self._connexion.send_command(CommandCode.HANDSHAKE)
        code = self._connexion.read_command()
        logger.info('Handshake received code: %s', code)
        return code == CommandCode.CONNECTED

    def send_command(self, command_code: CommandCode, *args, **kwargs):
        """
        Sends the given command.

        Args:
            command_code (CommandCode)
        """
        self._connexion.send_command(command_code, *args, **kwargs)


# Globally available boards.
BOARDS: dict[int, AbstractBoard] = {}


# @todo Initialize boards from the configuration.
def init():
    """ Initializes the BOARDS structure with available boards from config YAML files. """
    print(' > Init boards')
    BOARDS[1] = AbstractBoard('LEFT A', 'COM3')
    BOARDS[1].open()
    BOARDS[2] = AbstractBoard('RIGHT B', 'COM4')
    BOARDS[2].open()


def close():
    """ Closes properly the board' connection. """
    print(' > Close boards connection')
    for _, board in BOARDS.items():
        board.close()


def add_board(board: AbstractBoard):
    """ Register a new available board. """
    if BOARDS[board.id]:
        raise BoardException('Cannot add in BOARDS: board already exists in BOARDS.')
    BOARDS[board.id] = board


def update_board(board: AbstractBoard):
    """ Register a new available board. """
    if not BOARDS[board.id]:
        raise BoardException('Cannot update BOARDS: board do not exists in BOARDS.')
    BOARDS[board.id] = board


__all__ = ["BOARDS", "AbstractBoard", "BoardException", "init", "add_board", "update_board", "arduino"]
