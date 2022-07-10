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

from abc import abstractmethod

from hermes.core import logger
from hermes.core.plugins import AbstractPlugin
from hermes.core.protocols import AbstractProtocol
from hermes.core.struct import MetaPluginType


class BoardException(Exception):
    """ Base class for board related exceptions. """


class AbstractBoard(AbstractPlugin, metaclass=MetaPluginType):
    """ Handles the serial communication with an external board. """

    def __init__(self, name):
        super().__init__(name)
        self.connected: bool = False
        self._connexion: AbstractProtocol

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

    # @todo how to handle handshake from a board ? => the board should probably request it.
    # @abstractmethod
    # @func_set_timeout(1)
    # def handshake(self) -> bool:
    #     """ Performs handshake between the board and the application. """

    @abstractmethod
    def send(self, data: bytearray):
        """
        Sends the given data (via the internal protocol)

        Args:
            data (bytearray) An array of byte to transfer.
        """

    def __del__(self):
        logger.info(f' > Close board {self.id}')
        self.close()


__all__ = ["AbstractBoard", "BoardException"]
