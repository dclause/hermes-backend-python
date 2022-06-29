""" Core/Boards package

Contains anything related to configurable boards.
Currently, only arduino boards are supported.

Boards can be created from configs file leaving in the config/boards directory. Each board YAML file must validate the
schema provided within this package.
Boards are detected when the package is imported for the first time and globally available by import.

Examples:
    `from hermes.core.boards import BOARDS`

"""
from abc import abstractmethod

from func_timeout import func_set_timeout

from hermes.core import logger
from hermes.core.commands.blink import CommandCode
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class BoardException(Exception):
    """ Base class for board related exceptions. """


class AbstractBoard(AbstractPlugin, metaclass=MetaPluginType):
    """ Handles the serial communication with an external board. """

    @abstractmethod
    def open(self) -> bool:
        """
        Tries to open serial port with Arduino given the current Serial configuration.
        If not port is specified, it will be automatically detected

        Returns:
            bool

        Raises:
            SerialException: Raised if the given serial_port does not exist or cannot be opened
        """

    @abstractmethod
    def close(self) -> bool:
        """ Closes the connexion. """

    @abstractmethod
    @func_set_timeout(1)
    def handshake(self) -> bool:
        """ Performs handshake between the board and the application. """

    @abstractmethod
    def send_command(self, command_code: CommandCode, *args, **kwargs):
        """
        Sends the given command.

        Args:
            command_code (CommandCode)
        """

    def __del__(self):
        logger.info(' > Close board %s', str(self.id))
        self.close()


__all__ = ["AbstractBoard", "BoardException"]
