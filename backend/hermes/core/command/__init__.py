""" Commands package """
import glob
import importlib
from enum import IntEnum
from os import scandir
from os.path import dirname, join, basename, isfile

from hermes.core.struct import MetaPluginType, MetaSingleton


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
    SERVO = 41  # ascii )

    ######
    # 70 - 97: commands related to sensors/inputs

    ######
    # 98 - 126: commands related to passive components (displays, leds, etc...)
    BLINK = 98  # ascii: b


class AbstractCommand(metaclass=MetaPluginType):
    """ Manages plugins of type commands. """

    def __init__(self, code: CommandCode, name: str):
        self.code: CommandCode = code
        self.name: str = name

    def __str__(self):
        return f'Command {self.name}'

    def send(self, connexion):
        """ Sends the command. """

    def receive(self, connexion):
        """ Reads the additional parameters sent with the command. """

    # @logthis
    def process(self):
        """ Processes the command """


class CommandFactory(metaclass=MetaSingleton):
    """ Command factory class: instantiates a Command of a given type """

    def __init__(self):
        self.__commands: dict[CommandCode, AbstractCommand] = {}

        # Self registers all AbstractCommand defined plugins.
        for command in AbstractCommand.plugins:
            self.__commands[command().code] = command()

    def get_by_code(self, command_code: CommandCode) -> AbstractCommand | None:
        """ Instantiates a AbstractCommand based on a given CommandCode

        Args:
            command_code (CommandCode): The CommandCode of the Command to instantiate.
        Returns:
            AbstractCommand | None

        See Also:
            :class:`CommandCode`
        """
        return self.__commands.get(command_code)

    def get_by_name(self, name: str) -> AbstractCommand | None:
        """ Instantiates a AbstractCommand based on a given name

        Args
            name (str): The name of the Command to instantiate.
        Returns
            AbstractCommand or None

        See Also:
            :class:`CommandCode`
        """
        return next((command for command in self.__commands.values() if getattr(command, 'name') == name), None)


__ALL__ = ["AbstractCommand", "CommandCode", "CommandFactory"]

# Auto-import all commands within the directory and happen it to __ALL__.
# By doing so, we let the commands to auto-register to the factory.
# @see CommandFactory
# @see MetaPluginType
modules = glob.glob(join(dirname(__file__), "*.py"))
for f in modules:
    if isfile(f) and not f.endswith('__init__.py'):
        module = basename(f)[:-3]
        importlib.import_module(f'hermes.core.command.{module}')
        __ALL__.append(module)
