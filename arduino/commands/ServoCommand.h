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

        ServoCommand() : AbstractCommand(2) {}

        String getName() const { return "SERVO"; }

        void process() {
            // uint8_t deviceId = this->payload_[0];
            uint8_t position = this->payload_[1];
            TRACE((String) F("Requested position: ") + (String) position);

        }
};

REGISTER_COMMAND(CommandCode::SERVO, ServoCommand)

#endif // ARDUINO_SERVO_COMMAND_H
