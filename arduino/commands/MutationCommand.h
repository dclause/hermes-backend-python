#ifndef ARDUINO_MUTATION_COMMAND_H
#define ARDUINO_MUTATION_COMMAND_H

#include <Arduino.h>

#include "../helper/debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"
#include "../devices/AbstractDevice.h"
#include "../devices/DeviceManager.h"


/**
 * MUTATION Command: create/patch a command and store it to command manager if it is a runnable.
 *
 * @see CommandCode::MUTATION
 */
class MutationCommand : public AbstractCommand {
    COMMAND_DECLARATION

    public:

        MutationCommand() : AbstractCommand(1) {}

        String getName() const override { return "Mutation"; }

        void executePayload(uint8_t *payload) override {
            TRACE("-----------");
            TRACE("Process MUTATION command:");

            AbstractDevice *device = DeviceManager::getInstance().getDevice(payload[0]);
            if (device == NULL) {
                TRACE("  > Unfined command to mutate: " + String(payload[0]));
                return;
            }
            if (!device->isRunnable()) {
                TRACE("  > Cannot mutate non runnable: " + String(*device));
                return;
            }

            device->process();
        }
};

REGISTER_COMMAND(CommandCode::MUTATION, MutationCommand)

#endif  // ARDUINO_MUTATION_COMMAND_H
