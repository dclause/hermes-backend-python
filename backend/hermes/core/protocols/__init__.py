"""
Protocol communication package.
This package contains all implemented communication protocols provided by default in HERMES.

A "communication protocol" defines a way for a board to communicate with this server, therefore a protocol is designed
to be embedded in a board (see AbstractBoard) and must implement the AbstractProtocol interface. (ex: SerialProtocol)
"""

from abc import abstractmethod

from hermes.core.struct import MetaPluginType


class ProtocolException(Exception):
    """ Base class for protocol related exceptions. """


class AbstractProtocol(metaclass=MetaPluginType):
    """ Abstract class representing a Connexion protocol connexion of some kind."""

    @abstractmethod
    def open(self) -> None:
        """
        Opens the connexion.

        Returns:
            self

        Raises:
             ConnexionException
        """

    @abstractmethod
    def close(self) -> None:
        """ Closes the connexion. """

    @abstractmethod
    def is_open(self) -> bool:
        """ Checks if the connexion is active. """

    @abstractmethod
    def read_byte(self) -> int:
        """
        Reads a single byte.

        Warnings:
            This method is blocking.

        Returns:
            int: The 8bit next byte in queue.
        """

    @abstractmethod
    def send(self, data: bytearray) -> None:
        """
        Sends data.

        Args:
            data (bytearray) An array of byte to send.
        """

    @abstractmethod
    # @func_set_timeout(1)
    def read_line(self) -> str:
        """
        Reads the input data until the next EOF is received.

        Warnings:
            This method timeouts after 1sec.

        Returns:
            str: The data.
        """


__ALL__ = ["AbstractProtocol", "ProtocolException"]
