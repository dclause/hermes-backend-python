""" Defines semantic message byte values. """

from enum import IntEnum


# @todo export this enum to a single 'knowledge dictionary' file and create a code generator to make it.
# The purpose would be to not repeat the enum thought all languages and parts of the project.
# @see backend/hermes/core/messages.py
# @see arduino/helper/dictionary.h
class MessageCode(IntEnum):
    """
    Defines the byte codes of semantic messages (commands, devices, etc...) that can be received/emitted.

    Each message will be cast to a 8bits integer, therefore at most 255 semantic messages can be interpreted.
    Messages are (tried to) grouped by logical packages and assign arbitrarily a number.

    Warnings:
    --------
        Every number from 0 to 255 can be used for exchanges.

        A few numbers can be generated as "noise" in the serial pipe and should be thus avoided.
        These noises mainly happens when debugging the arduino code from the monitor. That is the reason they are
        for specific purposes:
          - 0 is ASCII [NULL] char: it is sent by Arduino IDE monitor when baudrate is changed
          - 10 is ASCII [EndOfLine] char: it is sent by Arduino IDE monitor on each data sent.
          - 35 is ASCII # char: is used to send debug data that should be ignored.

        @todo implement the following
        The values in this file must match with the values in the MessageCode.h file in the arduino project. A script is
        provided in order to help to main the files in sync.
        (@see messagecode.py in the scripts folder on the root mono-repo)

    Notes:
    -----
        Command code are maps to actual commands via the CommandFactory class.

    See Also:
    --------
        :file: scripts/messagecode.py
        :class:`CommandFactory`
    """

    ######
    # Reserved
    END_OF_LINE = 10  # Reserved @see attention point above

    ######
    # COMMANDS
    # 0 - 40: codes related to generic commands.
    VOID = 0  # Reserved @see attention point above
    DEBUG = 35  # Reserved @see arduino folder ioserial.h
    ACK = 11
    HANDSHAKE = 12
    CONNECTED = 13
    PATCH = 20
    MUTATION = 21
    # /!\ Skipped 35 for DEBUG.

    ######
    # DEVICES
    BOOLEAN_OUTPUT = 41
    SERVO = 42

    ######
    BOOLEAN_INPUT = 141
