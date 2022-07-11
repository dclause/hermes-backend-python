#ifndef ARDUINO_PATCH_COMMAND_H
#define ARDUINO_PATCH_COMMAND_H

#include <Arduino.h>

#include "../debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"
#include "../devices/AbstractDevice.h"
#include "../devices/DeviceCode.h"
#include "../devices/DeviceFactory.h"
#include "../devices/DeviceManager.h"

/**
 * PATCH Command: create/patch a device to device manager.
 *
 * @see CommandCode::PATCH
 */
class PatchCommand : public AbstractCommand {
    COMMAND_DECLARATION

    public:

        PatchCommand() : AbstractCommand(-1) {}

        String getName() const { return "Patch"; }

        void process() {
            TRACE((String) F("Process Patch command."));
            // Build a device from its code using the factory.
            const DeviceCode deviceCode = (DeviceCode) this->payload_[0];
            AbstractDevice *device = DeviceFactory::getInstance().createDevice(deviceCode);
            // Fills from the payload.
            device->fromBytes(this->payload_);
            // Store in the manager for later.
            DeviceManager::getInstance().addDevice(device);

            TRACE(DeviceManager::getInstance());
        }
};

REGISTER_COMMAND(CommandCode::PATCH, PatchCommand)

#endif  // ARDUINO_PATCH_COMMAND_H
