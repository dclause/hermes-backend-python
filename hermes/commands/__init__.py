"""
Commands package.
This package contains all implemented commands provided by default in HERMES.

A command is an action requested from and/or to a device/board. It can come from:
    - a device/board to be executed by the server (ex: DEBUG)
    - the server for a client (ex: HANDSHAKE)
    - the server to a board (ex: SERVO)
or any combination of those.
@see Device definition in devices package.

A command is represented by a unique 8bit identifier. Those are defined via the MessageCode enum.

Commands are detected when the package is imported for the first time and globally available via the commandFactory.
"""
from abc import abstractmethod
from typing import Any

from hermes.core import logger
from hermes.core.dictionary import MessageCode
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaSingleton, MetaPluginType


class CommandException(Exception):
    """ Base class for command related exceptions. """


class AbstractCommand(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    def __init__(self):
        super().__init__()
        self.default: Any = None
        self.value: Any = None

    @property
    @abstractmethod
    def code(self) -> MessageCode:
        """ Each command type must be a 8bit code from the MessageCode dictionary. """

    def receive(self, connexion):
        """ Reads the additional data sent with the command. """

    def process(self):
        """ Processes the command """

    def __str__(self):
        return f'Command {self.name}'


class CommandFactory(metaclass=MetaSingleton):
    """ Command factory class: instantiates a Command of a given type """

    def __init__(self):
        self.__commands: dict[MessageCode, AbstractCommand] = {}

        # Self registers all AbstractCommand defined plugins.
        for command in AbstractCommand.plugins:
            self.__commands[command().code] = command()

    def get_by_code(self, code: MessageCode) -> AbstractCommand | None:
        """ Instantiates a AbstractCommand based on a given MessageCode

        Args:
            code (MessageCode): The MessageCode of the Command to instantiate.
        Returns:
            AbstractCommand | None
        Raises:
            CommandException: the command code does not exist.

        See Also:
            :class:`MessageCode`
        """
        command = self.__commands.get(code)
        if command is None:
            logger.error(f'Command {code} do not exists.')
            raise CommandException(f'Command with code `{code}` do not exists.')
        return command

    def get_by_name(self, name: str) -> AbstractCommand | None:
        """ Instantiates a AbstractCommand based on a given name

        Args
            name (str): The name of the Command to instantiate.
        Returns
            AbstractCommand or None
        Raises:
            CommandException: the command name does not exist.

        See Also:
            :class:`MessageCode`
        """
        command = next((command for command in self.__commands.values() if getattr(command, 'name') == name), None)
        if command is None:
            logger.error(f'Command {name} do not exists.')
            raise CommandException(f'Command with name `{name}` do not exists.')
        return command


__ALL__ = ['AbstractCommand', 'CommandFactory', 'CommandException']
