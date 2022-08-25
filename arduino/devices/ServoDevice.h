#ifndef ARDUINO_SERVO_DEVICE_H
#define ARDUINO_SERVO_DEVICE_H

#include <Servo.h>
#include "../helper/dictionary.h"
#include "AbstractDevice.h"
#include "DeviceFactory.h"

/**
 * SERVO Device: turns servo to given angle.
 *
 * @see MessageCode::SERVO
 */
class ServoDevice : public AbstractDevice {
    DEVICE_DECLARATION

    protected:
        uint8_t pin_;

        uint16_t default_position_ms_ = 928;
        float current_position_ms_ = 928;
        uint16_t target_position_ms_ = 928;

        Servo servo_;

        // "Security" delay_ms_ after we consider to be on target to detach the servo.
        // Expressed in milliseconds (ms).
        uint32_t delay_ms_ = 5000;   // 1sec.

        // tmin / tmax are the theoretical min/max position a servo can reach.
        // Often 0-180, but could be 0-360 in theory, hence it uses 16bits to express.
        uint16_t tmin_ = 0;
        uint16_t tmax_ = 180;
        // min / max are the restricted min/max positions this servo should reach according to
        // user settings. Usually chosen because of hardware robot constraints.
        // It could be 0-360 in theory, hence it uses 16bits to express.
        uint16_t min_ = 0;
        uint16_t max_ = 180;

        // Expressed in degree per second (°/sec)
        // Negative value means infinite.
        int16_t max_speed_ms_ = -1;
        int16_t max_acceleration_ms_ = -1;

        // Expressed in degree per second (°/sec)
        float current_speed_ms_ = 0;
        // Expressed in milliseconds (ms).
        uint32_t time_when_start_ms_ = 0;
        uint32_t time_when_stop_ms_ = 0;

    public:
        // We expect 2bytes payload as a position between 0-360° or 544-2400 microseconds (µs) needs 16bits of size to express.
        ServoDevice() : AbstractDevice(2) {}

        String getName() const { return "SERVO"; }

        void updateSettings(const uint8_t *payload) {
            AbstractDevice::updateSettings(payload);
            this->pin_ = payload[1];

            // All speed/position/accelerations are two bytes word (0 to 360°) we ensure here to have a non-possible
            // value, even for the case we use Servo ms (544 to 2400).

            uint16_t defaultPosition = this->readPosition_(payload[2], payload[3]);
            this->default_position_ms_ = map(defaultPosition,
                                             this->tmin_,
                                             this->tmax_,
                                             MIN_PULSE_WIDTH,
                                             MAX_PULSE_WIDTH);

            this->tmin_ = this->readPosition_(payload[4], payload[5]);
            this->tmax_ = this->readPosition_(payload[6], payload[7]);
            this->min_ = this->readPosition_(payload[8], payload[9]);
            this->max_ = this->readPosition_(payload[10], payload[11]);

            uint16_t maxSpeed = this->readPosition_(payload[12], payload[13]);
            this->max_speed_ms_ = map(maxSpeed,
                                      this->tmin_,
                                      this->tmax_,
                                      MIN_PULSE_WIDTH,
                                      MAX_PULSE_WIDTH) - MIN_PULSE_WIDTH;
            uint16_t maxAcceleration = this->readPosition_(payload[14], payload[15]);
            this->max_acceleration_ms_ = map(maxAcceleration,
                                             this->tmin_,
                                             this->tmax_,
                                             MIN_PULSE_WIDTH,
                                             MAX_PULSE_WIDTH) - MIN_PULSE_WIDTH;


            this->target_position_ms_ = default_position_ms_;
            this->current_position_ms_ = default_position_ms_;
            this->time_when_start_ms_ = 0;
            this->current_speed_ms_ = 0;
            this->servo_.attach(this->pin_);
            this->time_when_stop_ms_ = millis();
            TRACE(*this);
        };

        void executePayload(uint8_t *payload) {
            TRACE("-----------");
            TRACE("Process SERVO command:");
            uint16_t targetPosition = this->readPosition_(payload[0], payload[1]);
            // Cap with the min/max values (this should be done by caller, hence just be a security issue here)
            targetPosition = max(this->min_, targetPosition);
            targetPosition = min(this->max_, targetPosition);
            this->target_position_ms_ = map(targetPosition,
                                            this->tmin_,
                                            this->tmax_,
                                            MIN_PULSE_WIDTH,
                                            MAX_PULSE_WIDTH);


            // Attach the servo as we are now going to use it.
            this->servo_.attach(this->pin_);
            this->current_speed_ms_ = 0;
            this->time_when_start_ms_ = 0;
            this->time_when_stop_ms_ = 0;

            TRACE("  > Servo on PIN " + String(this->pin_) +
                  " requests position: " + String(targetPosition) + "(" + String(this->target_position_ms_) + ")"
            );
        }


        void doUpdate(const uint32_t current_time) {
            uint16_t deltaT = current_time - this->time_of_last_update_;

            if (this->current_position_ms_ != this->target_position_ms_) {

                // Start the movement:
                if (this->time_when_start_ms_ == 0) {
                    this->time_when_start_ms_ = current_time - 1;
                    TRACE(" - start movement at: " + String(this->time_when_start_ms_));
                    TRACE(" - current position (ms): " + String(this->current_position_ms_) +
                          "(" + String(this->target_position_ms_) + ")"
                    );
                }

                // If we have an acceleration: use it (acceleration is linear here), otherwise, use max_speed_ms_.
                if (this->max_acceleration_ms_ < 0) {
                    this->current_speed_ms_ = this->max_speed_ms_;
                } else {
                    this->current_speed_ms_ += this->max_acceleration_ms_ *
                                               (current_time - this->time_when_start_ms_) / 1000.0;
                    this->current_speed_ms_ = min(this->max_speed_ms_, this->current_speed_ms_);
                }
                TRACE(" - new speed: " + String(this->current_speed_ms_));

                // If we have a current speed: use it to limit the next_position.
                // Otherwise, the next position is the target position.
                if (this->current_speed_ms_ >= 0) {
                    int16_t remainingDeltaMs = this->current_position_ms_ - this->target_position_ms_;
                    TRACE(" - remainingDeltaMs (ms): " + String(remainingDeltaMs));
                    float step = this->current_speed_ms_ * deltaT / 1000.0;
                    if (remainingDeltaMs > 0) {
                        step *= -1;
                    }
                    TRACE(" - step (ms): " + String(step));
                    if (abs(remainingDeltaMs) > abs(step)) {
                        this->current_position_ms_ += step;
                    } else {
                        this->current_position_ms_ = this->target_position_ms_;
                        this->time_when_stop_ms_ = current_time;
                    }
                } else {
                    this->current_position_ms_ = this->target_position_ms_;
                    this->time_when_stop_ms_ = current_time;
                }
                TRACE(" - new position (ms): " + String(this->current_position_ms_) +
                      "(" + String(this->target_position_ms_) + ")"
                );

                this->servo_.writeMicroseconds((int) this->current_position_ms_);
            } else if (
                    this->servo_.attached() &&
                    this->time_when_stop_ms_ > 0 &&
                    (current_time - this->time_when_stop_ms_) > this->delay_ms_) {
                TRACE("== Time to detach ==");
                this->servo_.detach();
                this->time_when_start_ms_ = 0;
                this->current_speed_ms_ = 0;
            }
        };

        operator String() {
            return AbstractDevice::operator String() + "\n" +
                   "\t\tpin:" + String(this->pin_) + "\n" +
                   "\t\tdefault:" + String(this->default_position_ms_) + "\n" +
                   "\t\tcurrent:" + String(this->current_position_ms_) + "\n" +
                   "\t\trequest:" + String(this->target_position_ms_) + "\n" +
                   "\t\ttmin:" + String(this->tmin_) + "\n" +
                   "\t\ttmax:" + String(this->tmax_) + "\n" +
                   "\t\tmin:" + String(this->min_) + "\n" +
                   "\t\tmax:" + String(this->max_) + "\n" +
                   "\t\tmax speed:" + String(this->max_speed_ms_) + "\n" +
                   "\t\tmax acceleration:" + String(this->max_acceleration_ms_);
        }

    private:
        uint16_t readPosition_(uint8_t byte1, uint8_t byte2) {
            TRACE(String("ReadPosition:") + "\n" +
                  "\t\tbyte1:" + String(byte1) + '\n' +
                  "\t\tbyte2:" + String(byte2));
            return (byte1 << 8) | byte2;
        }
};

REGISTER_DEVICE(MessageCode::SERVO, ServoDevice)

#endif // ARDUINO_SERVO_DEVICE_H
