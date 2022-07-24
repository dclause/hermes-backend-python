#ifndef ARDUINO_IO_H
#define ARDUINO_IO_H

/**
 * IO files aim to provide a unified interface to read/write operation methods.
 *
 * This file is dedicated to Input/Output arduino serial operations.
 * (currently, it is the only supported communication protocol)
 *
 * By exposing a unified interface for IO operations, switching between io files (when implemented) will be
 * transparent for the main code. This is made to help supporting various communication protocols, may it be Serial
 * (as here) or WIFI (to be implementation) or else.
 */

#include <HardwareSerial.h>
#include "debugger.h"
#include "../commands/CommandCode.h"

#define BAUDRATE 115200

namespace IO {

    /**
     * Debugs the data on the serial monitor.
     *
     * @details
     * All debug strings must be wrapped as follow:
     *  - DEBUG byte (@see Order.h) to indicate the other hand of the Serial communication to avoid this.
     *  - a [SPACE] byte (value 32)
     *  - an arbitrarily long string
     *  - a [EndOfLine] byte (value 10)
     *
     * For instance if debug param info is "Hello World", the sent data are : "# Hello World"
     * # is the byte 32 registered as the DEBUG command which will be received and interpreted both
     * on server and arduino side as pure DEBUG.
     *
     * @param info
     */
    void debug(const String &info) {
        Serial.println("# " + info);
    }

    /**
     * Initializes the communication protocol.
     */
    void begin() {
        Serial.begin(BAUDRATE);
        TRACE("Opening IO communication at baudrate " + String(BAUDRATE));
    }

    /**
     * Clears the receive buffer.
     *
     * This operation is done by reading at everything currently available on the receive buffer, hence, may never end
     * if the sender is spamming at that moment.
     */
    void clear() {
        while (Serial.available() > 0) {
            Serial.read();
        }
    }

    /**
     *  Returns the available number of bytes in the receive buffer.
     */
    uint8_t available() {
        return Serial.available();
    }

    /**
     * Waits for incoming given amount of bytes from the serial port, or exit if timeout.
     *
     * @param num_bytes (uint8_t): The number of bytes to wait for.
     * @param timeout (uint32_t): The timeout (in milliseconds) for the whole operation.
     */
    void wait_for_bytes(const uint8_t length, const uint32_t timeout = 100) {
        const uint32_t startTime = millis();
        while ((Serial.available() < length) && (millis() - startTime < timeout)) {}
    }

    /**
     * Receives and casts an 8bit word to a CommandCode.
     *
     * @return CommandCode
     */
    CommandCode read_command() {
        const CommandCode code = static_cast<CommandCode>(Serial.read());
        TRACE("Command code received: " + String((uint8_t) code));
        return code;
    }

    /**
     * Reads a given amount of bytes from the serial port.
     *
     * @note  This is a copy of Serial.readBytes(buffer, length), but WITH NO TIMEOUT.
     * @note  Because it has no timeout, this method should always be used in conjunction with wait_for_bytes() to ensure
     * the given amount of bytes to read is available.
     *
     * @param buffer (uint8_t*) A buffer array of uint8_t where the result will be stored.
     * @param length (uint8_t) The number of bytes to read.
     */
    void read_bytes(uint8_t *buffer, const uint8_t length) {
        uint8_t index = 0;
        uint8_t byte;
        while (index < length) {
            byte = Serial.read();
            if (byte < 0) break;
            *buffer++ = (uint8_t) byte;// equivalent to buffer[i] = (int8_t) byte;
            index++;
        }
        TRACE("Data received: " + String((char *) (buffer)));
    }

    /**
     * Waits for incoming given amount of bytes from the serial port, or exit if timeout.
     *
     * @param num_bytes (uint8_t): The number of bytes to wait for.
     * @param timeout (uint32_t): The timeout (in milliseconds) for the whole operation.
     */
    String read_until_endl() {
        return Serial.readStringUntil((char) CommandCode::END_OF_LINE);
    }

    /**
     * Sends an 8bit word CommandCode.
     *
     * @param command (CommandCode)
     */
    void send_command(const CommandCode command) {
        TRACE("Send command: " + String((uint8_t) command));
        Serial.write(static_cast<uint8_t>(command));
    }

    /**
     * Sends the given amount of bytes to the serial port.
     *
     * @param buffer (uint8_t*) A buffer array of uint8_t of data to send.
     * @param length (uint8_t) The number of bytes to write.
     */
    void send_bytes(const uint8_t *buffer, const uint8_t length) {
        Serial.write(buffer, length);
    }

}// namespace IO

#endif// ARDUINO_IO_H