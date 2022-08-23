"""
Commands package.
This package contains all implemented commands provided by default in HERMES.

A command is an action requested from and/or to a device/board. It can come from:
    - a device/board to be executed by the server (ex: DEBUG)
    - the server for a client (ex: HANDSHAKE)
    - the server to a board (ex: SERVO)
or any combination of those.
@see Device definition in devices package.

A command is represented by a unique 8bit identifier. Those are defined via the CommandCode enum.

Commands are detected when the package is imported for the first time and globally available via the commandFactory.
"""
from abc import abstractmethod
from enum import IntEnum
from typing import Any

from hermes.core import logger, config
from hermes.core.plugins import AbstractPlugin
from hermes.core.struct import MetaPluginType, MetaSingleton


class CommandException(Exception):
    """ Base class for command related exceptions. """


# @todo export this enum to a single 'knowledge dictionary' file and create a code generator to make it.
# The purpose would be to not repeat the enum thought all languages and parts of the project.
# @see frontend/composables/commands.ts
# @see backend/hermes/core/commands/__init__/py
# @see arduino/Commands/CommandCode.h

class CommandCode(IntEnum):
    """ Defines the command codes that can be sent/received.

    Each command will be cast to a 8bits integer, therefore at most 255 commands can be interpreted.
    Commands are (tried to) grouped by logical packages and assign arbitrarily a number.

    Warnings:
        Every number from 0 to 255 can be used for exchanges.

        A few numbers can be generated as "noise" in the serial pipe and should be thus avoided.
        These noises mainly happens when debugging the arduino code from the monitor. That is the reason they are
        for specific purposes:
          - 0 is ASCII [NULL] char: it is sent by Arduino IDE monitor when baudrate is changed
          - 10 is ASCII [EndOfLine] char: it is sent by Arduino IDE monitor on each data sent.
          - 35 is ASCII # char: is used to send debug data that should be ignored.

        The values in this file must match with the values in the MessageCode.h file in the arduino project. A script is
        provided in order to help to main the files in sync.
        (@see messagecode.py in the scripts folder on the root mono-repo)

    Notes:
        Command code are maps to actual commands via the CommandFactory class.

    See Also:
        :file: scripts/messagecode.py
        :class:`CommandFactory`
    """

    ######
    # Reserved
    VOID = 0  # Reserved @see attention point above
    END_OF_LINE = 10  # Reserved @see attention point above
    DEBUG = 35  # Reserved @see arduino folder ioserial.h

    ######
    # 0 to 40: generic purposes.
    # /!\ Skipped 0 for VOID.
    # /!\ Skipped 10 for END_OF_LINE.
    ACK = 11
    HANDSHAKE = 12
    CONNECTED = 13
    PATCH = 14
    MUTATION = 15
    # /!\ Skipped 35 for DEBUG.

    ######
    # 41 - 140: codes related to commands (for actuators).
    BOOLEAN_ACTION = 41
    SERVO = 42
    BLINK = 43
    ON_OFF = 44

    ######
    # 141 - 140: codes related to inputs (for sensors).
    BOOLEAN_INPUT = 141


class AbstractCommand(AbstractPlugin, metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    def __init__(self):
        super().__init__()
        self.default: Any = None
        self.value: Any = None

    @property
    @abstractmethod
    def code(self) -> CommandCode:
        """ Each command type must have a 8bit code from the CommandCode dictionary. """

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
            header = bytearray([CommandCode.MUTATION])
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
        self.__commands: dict[CommandCode, AbstractCommand] = {}

        # Self registers all AbstractCommand defined plugins.
        for command in AbstractCommand.plugins:
            self.__commands[command().code] = command()

    def get_by_code(self, code: CommandCode) -> AbstractCommand | None:
        """ Instantiates a AbstractCommand based on a given CommandCode

        Args:
            code (CommandCode): The CommandCode of the Command to instantiate.
        Returns:
            AbstractCommand | None
        Raises:
            CommandException: the command code does not exist.

        See Also:
            :class:`CommandCode`
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
            :class:`CommandCode`
        """
        command = next((command for command in self.__commands.values() if getattr(command, 'name') == name), None)
        if command is None:
            logger.error(f'Command {name} do not exists.')
            raise CommandException(f'Command with name `{name}` do not exists.')
        return command


__ALL__ = ["AbstractCommand", "CommandCode", "CommandFactory", "CommandException"]
