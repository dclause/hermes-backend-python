#ifndef ARDUINO_SERVO_COMMAND_H
#define ARDUINO_SERVO_COMMAND_H

#include <Servo.h>
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
        uint32_t delay_between_updates_ = -1;

        Servo servo_;

        uint16_t min_ = 0;
        uint16_t max_ = 180; // @todo configurable

    public:

        // todo: explain why 2 (16bits position)
        ServoCommand() : AbstractCommand(2) {}

        String getName() const { return "SERVO"; }

        bool isRunnable() const { return true; }

        void updateFromPayload(const uint8_t *payload) {
            AbstractCommand::updateFromPayload(payload);
            this->pin_ = payload[1];
            this->default_position_ = this->readPosition_(payload[2], payload[3]);
            this->requested_position_ = this->default_position_;
            // @todo why ?
            this->current_position_ = 65535;
            TRACE(*this);
        };

        void executePayload(uint8_t *payload) {
            TRACE("-----------");
            TRACE("Process SERVO command:");
            this->requested_position_ = this->readPosition_(payload[0], payload[1]);
            // Cap with the min/max values (this should be done by caller, hence just be a security issue here)
            // @todo this should be min/max indeed, not tmin, tmax to be introduced.
            this->requested_position_ = max(this->min_, this->requested_position_);
            this->requested_position_ = min(this->max_, this->requested_position_);

            // Attach the servo as we are now going to use it.
            this->servo_.attach(this->pin_);
            TRACE("  > Servo on PIN " +
                  String(this->pin_) +
                  " requests position: " +
                  String(this->requested_position_));
        }

        void update() {
            uint32_t currentTime = millis();
            if (this->shouldPerformNextTick(currentTime)) {
                this->nextTick();
                this->time_of_last_update_ = currentTime;
            }
        }

        bool shouldPerformNextTick(const uint32_t current_time) {
            return current_time - this->time_of_last_update_ >= this->delay_between_updates_;
        }

        void nextTick() {
            if (this->current_position_ != this->requested_position_) {
                // @todo this should be tmin, tmax to be introduced.
                uint32_t servoPos = map(this->requested_position_,
                                        this->min_,
                                        this->max_,
                                        MIN_PULSE_WIDTH,
                                        MAX_PULSE_WIDTH);
                this->servo_.writeMicroseconds(servoPos);
            }
        };

        operator String() {
            return AbstractCommand::operator String() + "\n" +
                   "\t\tpin:" + String(this->pin_) + "\n" +
                   "\t\tdefault:" + String(this->default_position_) + "\n" +
                   "\t\tcurrent:" + String(this->current_position_) + "\n" +
                   "\t\trequest:" + String(this->requested_position_);
        }

    private:

        uint16_t readPosition_(uint8_t byte1, uint8_t byte2) {
            TRACE(String("ReadPosition:") + "\n" +
                  "\t\tbyte1:" + String(byte1) + '\n' +
                  "\t\tbyte2:" + String(byte2));
            return (byte1 << 8) | byte2;
        }
};

REGISTER_COMMAND(CommandCode::SERVO, ServoCommand)

#endif // ARDUINO_SERVO_COMMAND_H
