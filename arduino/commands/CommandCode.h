#ifndef ARDUINO_COMMAND_CODE_H
#define ARDUINO_COMMAND_CODE_H

#include <Arduino.h>

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
 * Commands are (tried to) grouped by logical packages and assign arbitrarily a number.
 *
 * @attention
 * Every number from 0 to 255 can be used in theory at runtime for exchanges.
 * However, for debugging purposes, it is much more convenience to use printable characters to be used in the monitor,
 * hence values from 33 to 126.
 * To get the ascii equivalents, run code at https://docs.arduino.cc/built-in-examples/communication/ASCIITable
 *
 * A few numbers can be generated as "noise" in the serial pipe and should be thus avoided.
 * Theses noises mainly happens when debugging the arduino code from the monitor. Using those would therefore
 * generate noise when debugging via the monitor console.
 * - 0 is ASCII [NULL] char: it is sent by Arduino IDE monitor when baudrate is changed.
 * - 10 is ASCII [EndOfLine] char: it is sent by Arduino IDE monitor on each data sent.
 */
enum class CommandCode : uint8_t {

    // ######
    // Reserved
    VOID = 0,        // Reserved @see attention point above
    DEBUG = 35,      // Reserved @see debugger.h
    RESERVED = 10,   // Reserved @see attention point above

    // ######
    // 33 to 40: generic purposes.
    HANDSHAKE = 33,     // ascii: !
    CONNECTED = 34,     // ascii: "
    // /!\ Skipped 35 for DEBUG.
    ACK = 36,           // ascii: $

    // ######
    // 41 - 69: commands related to actuators.
    SERVO = 41,         // ascii: )

    // ######
    // 70 - 97: commands related to sensors/inputs

    // ######
    // 98 - 126: commands related to passive components (displays, LEDs, etc...)
    BLINK = 98          // ascii: b
};

typedef enum CommandCode CommandCode;

#endif // ARDUINO_COMMAND_CODE_H
