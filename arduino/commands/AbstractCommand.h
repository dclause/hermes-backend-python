#ifndef ARDUINO_COMMAND_H
#define ARDUINO_COMMAND_H

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
    public:
        virtual ~AbstractCommand() = default;

        /**
         * Returns a human readable name for the command.
         *
         * @return String
         */
        virtual String getName() const = 0;

        // @todo implement sending the command.
        // virtual void send() = 0;

        // @todo implement receiving parameters.
        // virtual void receive() = 0;

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

#endif // ARDUINO_COMMAND_H
