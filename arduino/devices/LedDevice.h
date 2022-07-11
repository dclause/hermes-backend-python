#ifndef ARDUINO_LED_DEVICE_H
#define ARDUINO_LED_DEVICE_H

#include <Arduino.h>

#include "../debugger.h"
#include "AbstractDevice.h"
#include "DeviceCode.h"
#include "DeviceFactory.h"

/**
 * LED Device.
 *
 * @see DeviceCode::LED
 */
class LedDevice : public AbstractDevice {
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
                   String(F(" pin:")) + (String) this->pin_ +
                   String(F(" default:")) + (String) this->default_;
        }
};

REGISTER_DEVICE(DeviceCode::LED, LedDevice)

#endif  // ARDUINO_LED_DEVICE_H
