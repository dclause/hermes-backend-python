#ifndef ARDUINO_DIGITAL_WRITE_DEVICE_H
#define ARDUINO_DIGITAL_WRITE_DEVICE_H

#include <Arduino.h>

#include "../helper/debugger.h"
#include "../helper/dictionary.h"
#include "AbstractDevice.h"
#include "DeviceFactory.h"

/**
 * DIGITAL_WRITE Device: toggle a digital pin write.
 *
 * @see MessageCode::DIGITAL_WRITE
 */
class DigitalWriteDevice : public AbstractDevice {
    DEVICE_DECLARATION

    public:

        DigitalWriteDevice() : AbstractDevice(2) {}

        String getName() const { return "DigitalWrite"; }

        void executePayload(uint8_t *payload) {
            TRACE("-----------");
            TRACE("Process DIGITAL_WRITE device:");

            uint8_t pin = payload[0];
            uint8_t value = payload[1];

            TRACE("  > Set pin " + String(pin) + " to: " + String(value));

            pinMode(pin, OUTPUT);
            digitalWrite(pin, value);
            TRACE("-----------");
        }
};

REGISTER_DEVICE(MessageCode::DIGITAL_WRITE, DigitalWriteDevice)

#endif  // ARDUINO_DIGITAL_WRITE_DEVICE_H
