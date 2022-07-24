#ifndef ARDUINO_COMMAND_H
#define ARDUINO_COMMAND_H

#include "../helper/debugger.h"
#include "../helper/ioserial.h"
#include <Arduino.h>


/**
 * Class AbstractCommand: all commands must implement this class.
 *
 * A command ca be:
 *  - An action that is required by the master to be done on the slave board.
 *      Ex.: turn a motor, orientate a servomotor, light a led...
 *  - An input that is required to be read and sent back to the master.
 *      Ex.: value of a push button, a PIR sensor, a distance sensor...
 *  - A generic purpose command, generally for the protocol itself.
 *      Ex.: a heartbeat, a handshake, an ACK, etc...
 *
 * A command can either be received (from the backend) or sent (to the backend).
 *
 * A command can be called "Runnable" if its execution is time dependent and should not be blocking.
 *      Ex.: Turning a servo takes time and we do want the whole robot to hold-on until done. Therefore the servo command
 *      is called "Runnable" and implements an update() mechanism that is a function time-dependent.
 *
 * A command is a suite of 8bits word:
 *  - starting with an uint8_t (one of the CommandCode dictionary) that will be mapped to the appropriate class by
 *  the CommandFactory.
 *  - followed by a payload which is an arbitrary number of bytes for arguments that are read by the receivePayload_().
 *
 * @note
 * Command codes are mapped to actual commands via the CommandFactory by registering the command class to the factory
 * keyed by the appropriate command code. This is done via the conjunction usage of the macros `COMMAND_DECLARATION`
 * and `REGISTER_COMMAND(N, T)`.
 * @see CommandFactory.h
 */
class AbstractCommand {
    protected:
        uint8_t id_ = 0;
        int expected_payload_size_;
        unsigned int effective_payload_size_;
        uint8_t *payload_;

    public:

        AbstractCommand(const int expected_payload_size = 0) :
                expected_payload_size_(expected_payload_size),
                effective_payload_size_(expected_payload_size ? expected_payload_size : 0) {
            if (expected_payload_size > 0) {
                this->payload_ = new uint8_t[expected_payload_size];
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
         * Returns the ID of this command.
         * We use a getter to the protected id_ attribute to make sure no-one changes this from the outside.
         * The only way to change the ID is via the updateFromPayload() method which ensures the ID can't be changed
         * afterward.
         *
         * @return String
         */
        uint8_t getId() const { return this->id_; };

        /**
         * Defines if the command is "Runnable".
         * (@see AbstractCommand description)
         *
         * @return boolean
         */
        virtual bool isRunnable() const { return false; }

        /**
         * Update the internal settings of a command from a bytes payload.
         *
         * @note This situation occurs when a handshake is made and the actions/inputs are declared by the backend to
         * the board (@see HandshakeCommand) or when an action/input is updated (for instance the servo speed is changed).
         *
         * @note The implementation below is pretty light. But as an AbstractCommand, we only know that payload[0] is the
         * the command id. Every implementation is responsible to override this method and know what the payload contains
         * for itself.
         *
         * @param payload
         */
        virtual void updateFromPayload(const uint8_t *payload) {
            if (this->id_ == 0) {
                this->id_ = payload[0];
            }
        }

        /**
         * Update the command internal state depending on time of the nextTick.
         */
        void nextTick() {};

        /**
         * Processes the command when received from the serial port. That means receive the payload and execute it.
         */
        void process() {
            this->receivePayload_();
            this->executePayload(this->payload_);
        };

        /**
         * Executes the command using the given payload.
         *
         * @param payload (uint8_t*)
         */
        virtual void executePayload(uint8_t *payload) = 0;

        /**
         * Stringifies the command for debug purpose.
         *
         * @return String
         */
        operator String() const {
            return "Command (" + String(this->getId()) + ") " + this->getName() + " ";
        }

    private:

        /**
         * Load the expected data in the internal payload.
         * The amount of data loaded is defined by the expected_payload_size_ variable for the command, or the given data
         * size as first byte sent after command code.
         * ex: 33 26 1 2 3 .... 26 would solve to a HANDSHAKE (33) with 26 bytes or data (1...26)
         *
         * The maximum amount of data sent is 255 bytes.
         */
        void receivePayload_() {
            if (this->expected_payload_size_ > 0) {
                IO::wait_for_bytes(this->expected_payload_size_);
                IO::read_bytes(this->payload_, this->expected_payload_size_);
            } else if (this->expected_payload_size_ < 0) {
                String data = IO::read_until_endl();
                this->effective_payload_size_ = data.length();
                this->payload_ = new uint8_t[this->effective_payload_size_];
                data.getBytes(this->payload_, this->expected_payload_size_);

                TRACE("Determine data size: " + String(this->effective_payload_size_));
                TRACE("Data received: " + data);
            }
        }
};

#endif// ARDUINO_COMMAND_H
