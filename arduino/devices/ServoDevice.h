#ifndef ARDUINO_SERVO_DEVICE_H
#define ARDUINO_SERVO_DEVICE_H

#include <Arduino.h>
#include "AbstractDevice.h"

/**
 * Servomotor device.
 *
 * @todo Specifications & implementation !
 */
class ServoDevice : public AbstractDevice {
        String name_ = "SERVO";
};

#endif // ARDUINO_SERVO_DEVICE_H
