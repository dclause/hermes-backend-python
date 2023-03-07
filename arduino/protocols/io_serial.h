#ifndef ARDUINO_IO_SERIAL_H
#define ARDUINO_IO_SERIAL_H

#ifdef USE_SERIAL_PROTOCOL

/**
 * SERIAL protocol for arduino-to-server communication.
 *
 * IO files aim to provide a unified interface to read/write operations. This allows
 * the protocol to be transparently switched from the main .ino code.
 */

#error USE_SERIAL_PROTOCOL

#include <HardwareSerial.h>
#include "../helper/debugger.h"
#include "../helper/dictionary.h"

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
    bool wait_for_bytes(const uint32_t length, const uint32_t timeout = 100) {
        const uint32_t startTime = millis();
        while (Serial.available() < length) {
            if ((millis() - startTime) >= timeout) {
                return false;
            }
        }
        return true;
    }

    /**
     * Receives and casts an 8bit word to a MessageCode.
     *
     * @return MessageCode
     */
    MessageCode read_command() {
        const MessageCode code = static_cast<MessageCode>(Serial.read());
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
            buffer[index] = (int8_t) byte;
            index++;
        }
    }

    /**
     * Waits for incoming given amount of bytes from the serial port, or exit if timeout.
     *
     * @param num_bytes (uint8_t): The number of bytes to wait for.
     * @param timeout (uint32_t): The timeout (in milliseconds) for the whole operation.
     */
    uint32_t read_until_endl(uint8_t *buffer) {
        uint32_t index = 0;
        uint8_t byte;
        while (wait_for_bytes(1)) {
            byte = Serial.read();
            if (byte < 0 || byte == ((uint8_t) MessageCode::END_OF_LINE)) break;
            buffer[index] = (int8_t) byte;
            index++;
            TRACE("read_until_endl:" + String(byte));
        }
        return index;
    }

    /**
     * Sends an 8bit word MessageCode.
     *
     * @param command (MessageCode)
     */
    void send_command(const MessageCode command) {
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

} // namespace IO

#endif // USE_SERIAL_PROTOCOL
#endif // ARDUINO_IO_SERIAL_H