#ifndef ARDUINO_DEVICE_H
#define ARDUINO_DEVICE_H

#include <Arduino.h>

/**
 * Class AbstractDevice: all devices must implement this class.
 *
 * A device is (generally) an actuator or a sensor connected to the board that can execute commands. Can be for
 * instance a servomotor, a led, etc...
 *
 * A device is responsible to store its configurations (pin usage, internal state, etc...) and execute the command it
 * is asked to do.
 *
 * @todo expand on the description once conception is done
 *
 * @todo convert to an abstract class as per AbstractCommand.
 */
class AbstractDevice {
    protected:
        uint8_t id_ = 0;
        String name_ = "(do not use)";

    public:
        AbstractDevice(uint8_t id, const String &name) : id_(id), name_(name) {}

        uint8_t getId() const { return this->id_; }

        String getName() const { return this->name_; }

        /**
         * Stringifies the data for debug purpose.
         *
         * @return String
         */
        operator String() {
            return String(F("AbstractDevice (")) + this->id_ + String(F(") ")) + this->name_;
        }
};

#endif // ARDUINO_DEVICE_H
