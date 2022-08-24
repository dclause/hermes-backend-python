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

from hermes.core import logger, config
from hermes.core.dictionary import MessageCode
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType, MetaSingleton


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
        """ Each command type must have a 8bit code from the MessageCode dictionary. """

    @abstractmethod
    def _get_settings(self) -> bytearray:
        """ Encodes the settings of the command as a byte array. """
        return bytearray()

    @abstractmethod
    def _get_mutation(self, value: any) -> bytearray:
        """ Encodes the given value as an array of bytes. """
        return bytearray([value])

    @property
    def _is_runnable(self) -> bool:
        """ Defines if the command is runnable. """
        return False

    def to_patch_payload(self) -> bytearray:
        """
        Returns the representation of the command as a bytearray.
        This is used to:
         - describes the command to the physical board during the handshake process.
         - changes the settings of a command
        @todo Build the settings
        """
        header = bytearray([self.code, self.id])
        settings = self._get_settings()
        return bytearray([len(settings) + 2]) + header + settings

    def send(self, board_id, value: any):
        """ Sends the command. """
        board = config.BOARDS[board_id]

        if not board.connected:
            if not board.open():
                raise CommandException(f'Board {board.id} ({board.name}) is not connected.')

        if self._is_runnable:
            header = bytearray([MessageCode.MUTATION])
        else:
            header = bytearray([self.code])
        data = self._get_mutation(value)
        board.send(header + data)

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


__ALL__ = ["AbstractCommand", "MessageCode", "CommandFactory", "CommandException"]
