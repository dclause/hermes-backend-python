#ifndef ARDUINO_COMMAND_H
#define ARDUINO_COMMAND_H

#include "../debugger.h"
#include "../helper/ioserial.h"
#include <Arduino.h>


/**
 * Class AbstractCommand: all commands must implement this class.
 *
 * A command is (generally) an action that is required by the master to be done on the slave board. Can be for
 * instance to turn a motor, orient a servomotor, light a led...
 *
 * A command can either be received or send.
 *
 * A command is a suite of 8bits word:
 *  > starting with an uint8_t (one of the CommandCode dictionary) that will be mapped to the appropriate class by
 *  the CommandFactory.
 *  > followed by an arbitrary number of bytes for arguments.
 *
 * @example
 * @todo add a simple yet not trivial example here, such as `LIGHT_ON pin` when done.
 *
 * @note
 * Command codes are mapped to actual commands via the CommandFactory by registering the command class to the factory
 * keyed by the appropriate command code. This is done via the conjunction usage of the macros `COMMAND_DECLARATION`
 * and `REGISTER_COMMAND(N, T)`.
 * @see CommandFactory.h
 */
class AbstractCommand {

    protected:
        int expected_payload_size_;
        unsigned int effective_payload_size_;
        uint8_t *payload_;

    public:
        AbstractCommand(const int expected_payload_size = 0) :
                expected_payload_size_(expected_payload_size),
                effective_payload_size_(expected_payload_size ? expected_payload_size : 0) {
            if (expected_payload_size > 0) {
                this->payload_ = static_cast<uint8_t *>(malloc(expected_payload_size * sizeof(uint8_t)));
            }
        }

        virtual ~AbstractCommand() {
            free(this->payload_);
            this->payload_ = NULL;
        };

        /**
         * Returns a human readable name for the command.
         *
         * @return String
         */
        virtual String getName() const = 0;

        /**
         * Load the expected data in the internal payload.
         * The amount of data loaded is defined by the expected_payload_size_ variable for the command, or the given data
         * size as first byte sent after command code.
         * ex: 33 26 1 2 3 .... 26 would solve to a HANDSHAKE (33) with 26 bytes or data (1...26)
         *
         * The maximum amount of data sent is 255 bytes.
         */
        void receive() {
            if (this->expected_payload_size_ > 0) {
                IO::wait_for_bytes(this->expected_payload_size_);
                IO::read_bytes(this->payload_, this->expected_payload_size_);
            } else if (this->expected_payload_size_ < 0) {
                String data = IO::read_until_endl();
                this->effective_payload_size_ = data.length();
                TRACE((String) F("Determine data size: ") + (String) this->effective_payload_size_);
                this->payload_ = static_cast<uint8_t *>(malloc(this->effective_payload_size_ * sizeof(uint8_t)));
                for (unsigned int i = 0; i < this->effective_payload_size_; i++) {
                    this->payload_[i] = (uint8_t) data[i];
                }
            }
        }

        /**
         * Processes the command when received from the serial port.
         */
        virtual void process() = 0;

        /**
             * Stringifies the command for debug purpose.
             *
             * @return String
             */
        operator String() const {
            return (String) F("Command ") + this->getName();
        }
};

#endif// ARDUINO_COMMAND_H
