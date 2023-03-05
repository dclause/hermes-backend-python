"""
Protocol communication package.
This package contains all implemented communication protocols provided by default in HERMES.

A "communication protocol" defines a way for a board to communicate with this server, therefore a protocol is designed
to be embedded in a board (see AbstractBoard) and must implement the AbstractProtocol interface. (ex: SerialProtocol)
"""

from abc import abstractmethod

from hermes.core.helpers import HermesError
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType


class ProtocolError(HermesError):
    """Base class for protocol related exceptions."""

    def __init__(self, name: str):
        super().__init__(f'Board {name}: Connexion could not be opened.')


class AbstractProtocol(AbstractPlugin, metaclass=MetaPluginType):
    """Abstract class representing a Connexion protocol connexion of some kind."""

    @abstractmethod
    def open(self) -> None:
        """
        Open the connexion.
        :raise ProtocolError: the connexion cannot be established.
        """

    @abstractmethod
    def close(self) -> None:
        """Close the connexion."""

    @abstractmethod
    def is_open(self) -> bool:
        """Check if the connexion is active."""

    @abstractmethod
    def read_byte(self) -> int:
        """
        Read a single byte - in a blocking way.
        :return int: The 8bit next byte in queue.
        """

    @abstractmethod
    def send(self, data: bytearray) -> None:
        """
        Send given data.
        :param bytearray data:  An array of byte to send.
        """

    @abstractmethod
    # @func_set_timeout(1)
    def read_line(self) -> str:
        """
        Read the input data until the next EOF is received.
        This method timeouts after 1sec.
        :return str: the data.
        """


__ALL__ = ['AbstractProtocol', 'ProtocolError']
