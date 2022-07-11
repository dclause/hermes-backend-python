#ifndef ARDUINO_DEVICE_CODE_H
#define ARDUINO_DEVICE_CODE_H

#include <Arduino.h>

/**
 * Defines the device codes to identify devices.
 *
 * @note
 * Device codes are mapped to actual devices via the DeviceFactory by registering the device class to the factory
 * keyed by the appropriate device code. This is done via the conjunction usage of the macros `DEVICE_DECLARATION`
 * and `REGISTER_DEVICE(N, T)`.
 * @see DeviceFactory.h
 *
 * @details
 * Each device must cast to an 8bits integer, therefore at most 255 devices can be interpreted. Device codes cannot
 * be edited later in time for compatibility purposes. Therefore, the list below may be unsorted as time goes on and
 * new device codes are added.
 */
enum class DeviceCode : uint8_t {
    LED = 1,
    SERVO = 2,
};

typedef enum DeviceCode DeviceCode;

#endif // ARDUINO_DEVICE_CODE_H
