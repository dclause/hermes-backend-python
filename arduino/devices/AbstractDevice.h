#ifndef ARDUINO_DEVICE_H
#define ARDUINO_DEVICE_H

#include <Arduino.h>
#include "../debugger.h"

/**
 * Class AbstractDevice: all devices must implement this class.
 *
 * A device is (generally) an actuator or a sensor connected to the board that can execute commands. Can be for
 * instance a servomotor, a led, etc...
 *
 * A device is responsible to store its configurations (pin usage, internal state, etc...) and execute the command it
 * is asked to do.
 */
class AbstractDevice {
    protected:
        uint8_t id_;

    public:
        AbstractDevice() {}

        virtual ~AbstractDevice() {}

        uint8_t getId() const { return this->id_; };

        /**
         * Returns a human readable name for the device.
         *
         * @return String
         */
        virtual String getName() const = 0;

        /**
         * Update the device with informations for a command payload.
         *
         * @note This is quote abstract typehint, but each device implementation should know how to use the patch payload
         * for itself. By default, the AbstractDevice know only about the code at payload[0] and the id at payload[1].
         * The rest of payload data are handling by device implementations.
         *
         * @param payload
         */
        virtual void fromBytes(const uint8_t *payload) {
            this->id_ = payload[1];
        };

        /**
         * Stringifies the data for debug purpose.
         *
         * @return String
         */
        virtual operator String() {
            return String(F("Device (")) + (String) this->id_ + String(F(") ")) + this->getName();
        }
};

#endif // ARDUINO_DEVICE_H
