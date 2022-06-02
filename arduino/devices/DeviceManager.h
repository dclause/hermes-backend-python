#ifndef ARDUINO_DEVICE_MANAGER_H
#define ARDUINO_DEVICE_MANAGER_H

#include <Arduino.h>
#include "../helper/map.h"
#include "AbstractDevice.h"

/**
 * Device manager: lists all know devices.
 */
class DeviceManager {
    private:
        DeviceManager() {};
        KeyValueMap<uint8_t, AbstractDevice> devices_;

    public:
        DeviceManager(const DeviceManager &) = delete;

        DeviceManager &operator=(const DeviceManager &) = delete;

        static DeviceManager &getInstance() {
            static DeviceManager instance;
            return instance;
        }

        /**
         * Deletes all known devices.
         */
        void clearDevices() {
            return this->devices_.clear();
        }

        /**
         * Returns all known devices.
         *
         * @return KeyValueMap<uint8_t, AbstractDevice>
         */
        KeyValueMap<uint8_t, AbstractDevice> getDevices() const {
            return this->devices_;
        }

        /**
         * Add a device to the known list.
         *
         * @param device AbstractDevice: a device.
         * @return bool: If the device as been stored properly.
         */
        bool addDevice(const AbstractDevice &device) {
            return this->devices_.add(device.getId(), device);
        }

        /**
         * Gets a device on teh list by its ID.
         * @param id
         * @return AbstractDevice
         */
        AbstractDevice getDevice(uint8_t id) {
            return this->devices_.getValue(id);
        }

        /**
         * Stringifies the command for debug purpose.
         *
         * @return String
         */
        operator String() {
            String log = (String) F("AbstractDevice Manager:\n");
            for (uint8_t i = 0; i < this->devices_.count(); i++) {
                AbstractDevice device = this->devices_.get(i)->value;
                log += (String) F("# - ") + (String) device + F("\n");
            }
            return log;
        }
};

#endif // ARDUINO_DEVICE_MANAGER_H
