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
        uint8_t payload_size_;
        uint8_t *payload_;

    public:
        AbstractCommand(const uint8_t payload_size = 0) : payload_(
                static_cast<uint8_t *>(malloc(payload_size * sizeof(uint8_t)))),
                                                          payload_size_(payload_size) {}

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

        void receive() {
            if (this->payload_size_) {
                IO::wait_for_bytes(this->payload_size_, 100);
                IO::read_bytes(payload_, this->payload_size_);
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
