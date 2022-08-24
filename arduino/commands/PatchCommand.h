#ifndef ARDUINO_PATCH_COMMAND_H
#define ARDUINO_PATCH_COMMAND_H

#include <Arduino.h>

#include "../helper/debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"
#include "../devices/AbstractDevice.h"
#include "../devices/DeviceFactory.h"
#include "../devices/DeviceManager.h"


/**
 * PATCH Command: create/patch a command and store it to command manager if it is a runnable.
 *
 * @see CommandCode::PATCH
 */
class PatchCommand : public AbstractCommand {
    COMMAND_DECLARATION

    public:

        PatchCommand() : AbstractCommand(-1) {}

        String getName() const override { return "Patch"; }

        void executePayload(uint8_t *payload) override {
            TRACE("-----------");
            TRACE("Process PATCH command:");

            // The payload received for a PATCH deviceToPatch always starts by the CommandCode of the deviceToPatch to patch.
            const CommandCode commandCode = static_cast<CommandCode>(payload[0]);
            TRACE(
                    "  > Received commandCode: " + String((uint8_t) commandCode));
            AbstractDevice *deviceToPatch = DeviceFactory::getInstance().createDevice(commandCode);
            if (deviceToPatch == NULL) {
                TRACE("  => PATCH abort: command not found.");
                return;
            }
            TRACE("  > Command to PATCH: " + String(*deviceToPatch));

            if (deviceToPatch->isRunnable()) {
                TRACE("  > CommandToPatch is runnable.");

                // The data to use is the PATCH payload minus the first bytes (CommandCode)
                uint8_t *data = payload + 1;

                // First check if the runnable is already declared.
                // NOTE: The payload for a runnable necessarily starts with ID at offset 1.
                TRACE("  > Search for existing runnable with ID: " + String(payload[1]));
                AbstractDevice *existingDevice = DeviceManager::getInstance().getDevice(payload[1]);
                if (existingDevice != NULL) {
                    TRACE("  > Runnable needs update.");
                    TRACE(
                            "  > Updated " + String(*existingDevice));
                    // @todo implement the update.
                } else {
                    TRACE("  > Runnable needs create.");
                    deviceToPatch->updateFromPayload(data);
                    DeviceManager::getInstance().addDevice(deviceToPatch);
                    TRACE(
                            "  > Created " + String(*deviceToPatch));
                }
            } else {
                // The data to use is the PATCH payload minus the two first bytes (CommandCode + ID)
                uint8_t *data = payload + 2;
                // In the case of a simple deviceToPatch, we execute right away the deviceToPatch.
                deviceToPatch->executePayload(data);
            }
        }
};

REGISTER_COMMAND(CommandCode::PATCH, PatchCommand)

#endif  // ARDUINO_PATCH_COMMAND_H
