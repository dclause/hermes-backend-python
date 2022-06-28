"""
Protocol communication definition.
"""

from abc import abstractmethod

from hermes.core.commands.blink import CommandCode
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
    def read_command(self) -> CommandCode:
        """
        Reads a command.

        Warnings:
            This method is blocking.

        Returns:
            CommandCode: The 8bit command code.
        """

    @abstractmethod
    def send_command(self, command_code: CommandCode, *args, **kwargs) -> None:
        """ Sends a command. """

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


__ALL__ = ["usbserial"]
