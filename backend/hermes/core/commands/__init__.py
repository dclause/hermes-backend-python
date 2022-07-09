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
from enum import IntEnum

from hermes.core import logger, config
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
        Every number from 0 to 255 can be used in theory at runtime for exchanges.

        However, for debugging purposes, it is much more convenience to use printable characters to be used in the
        monitor, hence values from 33 to 126.
        To get the ascii equivalents, run code at https://docs.arduino.cc/built-in-examples/communication/ASCIITable

        A few numbers can be generated as "noise" in the serial pipe and should be thus avoided.
        These noises mainly happens when debugging the arduino code from the monitor. Using those would therefore
         generate noise when debugging via the monitor console.
          - 0 is ASCII [NULL] char: it is sent by Arduino IDE monitor when baudrate is changed.
          - 10 is ASCII [EndOfLine] char: it is sent by Arduino IDE monitor on each data sent.

    Command code are maps to actual commands via the CommandFactory class.

    See Also:
         :class:`CommandFactory`
    """

    ######
    # Reserved
    VOID = 0  # Reserved @see attention point above
    DEBUG = 35  # Reserved @see debugger.h
    RESERVED = 10  # Reserved @see attention point above

    ######
    # 33 to 40: generic purposes.
    HANDSHAKE = 33  # ascii: !
    CONNECTED = 34  # ascii: "
    # /!\ Skipped 35 for DEBUG.
    ACK = 36  # ascii: $

    ######
    # 41 - 69: commands related to actuators.
    SERVO = 41  # ascii: )

    ######
    # 70 - 97: commands related to sensors/inputs

    ######
    # 98 - 126: commands related to passive components (displays, leds, etc...)
    BLINK = 98  # ascii: b
    ON_OFF = 99  # ascii: c


class AbstractCommand(metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    def __init__(self, code: CommandCode, name: str):
        self.code: CommandCode = code
        self.name: str = name
        self._payload: bytearray

    def __str__(self):
        return f'Command {self.name}'

    @classmethod
    def encode(cls, value: any) -> bytearray:
        """ Encodes the given value as an array of bytes. """
        return bytearray([value])

    def send(self, device_id: int, value: any):
        """ Sends the command. """
        device = config.DEVICES[device_id]
        header = bytearray([self.code, device.id])
        data = self.encode(value)
        config.BOARDS[device.board].send(header + data)

    def receive(self, connexion):
        """ Reads the additional parameters sent with the command. """

    def process(self):
        """ Processes the command """


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
