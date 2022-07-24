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
    public:

        String getName() const { return "SERVO"; }

        bool isRunnable() const { return true; }

        void fromBytes(const uint8_t *payload) {
            AbstractCommand::fromBytes(payload);
        };

        void executePayload(uint8_t *payload) {
            TRACE((String) F("Process Servo command."));

            // uint8_t deviceId = this->payload_[0];
            uint8_t position = payload_[1];

            TRACE((String) F("  > Requested position: ") + (String) position);

        }
};

REGISTER_COMMAND(CommandCode::SERVO, ServoCommand)

#endif // ARDUINO_SERVO_COMMAND_H
