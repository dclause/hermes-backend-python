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
    uint16_t default_position_;
    uint16_t current_position_;
    uint16_t requested_position_;
    uint32_t time_of_last_update_;
    uint32_t delay_between_updates_ = 1000;

    uint8_t min_ = 0;
    uint8_t max_ = 180;     // @todo handle servos with 300° of freedom

public:
    String getName() const { return "SERVO"; }

    bool isRunnable() const { return true; }

    void updateFromPayload(const uint8_t *payload) {
        AbstractCommand::updateFromPayload(payload);
        this->pin_ = payload[1];
        this->default_position_ = payload[2];
        this->requested_position_ = this->default_position_;
        this->current_position_ = 65535;
    };

    void executePayload(uint8_t *payload) {
        TRACE("-----------");
        TRACE("Process SERVO command:");
        this->requested_position_ = payload[1];
        TRACE("  > Requested position: " + String(this->requested_position_));
    }

    void nextTick() {
        uint32_t currentTime = millis();
        if (currentTime - time_of_last_update_ >= this->delay_between_updates_) {
            this->time_of_last_update_ = currentTime;
            // TODO
            IO::debug("update");
        }
        if (this->current_position_ != this->requested_position_) {
        }
    };

    operator String() {
        return AbstractCommand::operator String() + "\n" +
               "\t\tpin:" + String(this->pin_) +
               "\t\tdefault:" + String(this->default_position_) +
               "\t\tcurrent:" + String(this->current_position_) +
               "\t\trequest:" + String(this->requested_position_);
    }
};

REGISTER_COMMAND(CommandCode::SERVO, ServoCommand)

#endif // ARDUINO_SERVO_COMMAND_H
