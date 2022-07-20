#ifndef ARDUINO_COMMAND_CODE_H
#define ARDUINO_COMMAND_CODE_H

#include <Arduino.h>


/**
 * @todo export this enum to a single 'knowledge dictionary' file and create a code generator to make it.
 * @see frontend/composables/commands.ts
 * @see backend/hermes/core/commands/__init__/py
 * @see arduino/Commands/CommandCode.h
 */

/**
 * Defines the command codes that can be received/emitted.
 *
 * @note
 * Command codes are mapped to actual commands via the CommandFactory by registering the command class to the factory
 * keyed by the appropriate command code. This is done via the conjunction usage of the macros `COMMAND_DECLARATION`
 * and `REGISTER_COMMAND(N, T)`.
 * @see CommandFactory.h
 *
 * @details
 * Each command must cast to an 8bits integer, therefore at most 255 commands can be interpreted.
 * Commands are (tried to) grouped by logical packages but the numbers are assigned as development go in no particular
 * order.
 *
 * @attention
 * Every number from 0 to 255 can be used for exchanges.
 *
 * A few numbers can be generated as "noise" in the serial pipe and should be thus avoided.
 * These noises mainly happens when debugging the arduino code from the monitor. That is the reason they are
 * for specific purposes:
 *  - 0 is ASCII [NULL] char: it is sent by Arduino IDE monitor when baudrate is changed
 *  - 10 is ASCII [EndOfLine] char: it is sent by Arduino IDE monitor on each data sent.
 *  - 35 is ASCII # char: is used to send debug data that should be ignored.*
 *
 * The values in this file must match with the values in the MessageCode.h file in the arduino project. A script is
 * provided in order to help to main the files in sync.
 * (@see messagecode.py in the scripts folder on the root mono-repo)
 */
enum class CommandCode : uint8_t {

    // //////////
    // Reserved
    VOID = 0,  // Reserved @see attention point above
    END_OF_LINE = 10,  // Reserved @see attention point above
    DEBUG = 35,  // Reserved @see arduino folder ioserial.h

    // //////////
    // 0 to 40: generic purposes.
    // /!\ Skipped 0 for VOID.
    // /!\ Skipped 10 for END_OF_LINE.
    ACK = 11,
    HANDSHAKE = 12,
    CONNECTED = 13,
    PATCH = 14,
    // /!\ Skipped 35 for DEBUG.

    // //////////
    // 41 - 140: codes related to commands (for actuators).
    BOOLEAN_ACTION = 41,
    SERVO = 42,
    BLINK = 43,
    ON_OFF = 44,

    // //////////
    // 141 - 140: codes related to inputs (for sensors).
    BOOLEAN_INPUT = 141,
};

typedef enum CommandCode CommandCode;

#endif // ARDUINO_COMMAND_CODE_H
