#ifndef ARDUINO_SERVO_DEVICE_H
#define ARDUINO_SERVO_DEVICE_H

#include "../debugger.h"
#include "AbstractDevice.h"
#include "DeviceCode.h"
#include "DeviceFactory.h"


/**
 * Servomotor device.
 *
 * @todo Specifications & implementation !
 */
class ServoDevice : public AbstractDevice {
    DEVICE_DECLARATION

    protected:
        uint8_t pin_;
        bool default_;

    public:
        String getName() const { return "LedDevice"; }

        void fromBytes(const uint8_t *payload) {
            AbstractDevice::fromBytes(payload);
            this->pin_ = payload[2];
            this->default_ = (bool) payload[3];
        }

        operator String() {
            return AbstractDevice::operator String() +
                   " pin:" + String(this->pin_) +
                   " default:" + String(this->default_);
        }
};

REGISTER_DEVICE(CommandCode::SERVO, ServoDevice)

#endif // ARDUINO_SERVO_DEVICE_H
