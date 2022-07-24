#ifndef ARDUINO_SERVO_COMMAND_H
#define ARDUINO_SERVO_COMMAND_H

#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"

/**
 * SERVO Command: turns servo to given angle.
 *
 * @see CommandCode::SERVO
 */
class ServoCommand : public AbstractCommand {
    COMMAND_DECLARATION

    protected:
        uint8_t pin_;
        bool default_;

    public:
        String getName() const { return "SERVO"; }

        bool isRunnable() const { return true; }

        void fromBytes(const uint8_t *payload) {
            AbstractCommand::fromBytes(payload);
            this->pin_ = payload[1];
            this->default_ = payload[2];
        };

        void executePayload(uint8_t *payload) {
            TRACE("-----------");
            TRACE("Process SERVO command:");

            uint8_t position = payload[1];
            TRACE("  > Requested position: " + String(position));
        }

        operator String() {
            return AbstractCommand::operator String() + "\n" +
                   "\t\tpin:" + String(this->pin_) +
                   "\t\tdefault:" + String(this->default_);
        }
};

REGISTER_COMMAND(CommandCode::SERVO, ServoCommand)

#endif // ARDUINO_SERVO_COMMAND_H
