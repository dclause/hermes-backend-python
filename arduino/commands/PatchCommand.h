#ifndef ARDUINO_PATCH_COMMAND_H
#define ARDUINO_PATCH_COMMAND_H

#include <Arduino.h>

#include "../helper/debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"
#include "RunnableManager.h"


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

            // The payload received for a PATCH commandToPatch always starts by the CommandCode of the commandToPatch to patch.
            const CommandCode commandCode = static_cast<CommandCode>(payload[0]);
            TRACE(
                    "  > Received commandCode: " + String((uint8_t) commandCode));
            AbstractCommand *commandToPatch = CommandFactory::getInstance().createCommand(commandCode);
            if (commandToPatch == NULL) {
                TRACE("  => PATCH abort: command not found.");
            }
            TRACE("  > Command to PATCH: " + String(*commandToPatch));


            if (commandToPatch->isRunnable()) {
                TRACE("  > CommandToPatch is runnable.");

                // In the case of a runnable, we either create or patch the runnable in the RunnableManager.
                // The data to use is the PATCH payload minus the first byte (CommandCode)
                uint8_t *data = payload + 1;

                // First check if the runnable is already declared.
                // NOTE: The payload for a runnable necessarily starts with ID at offset 1, hence data at offset 0.
                TRACE("  > Search for existing runnable with ID: " + String(data[0]));
                AbstractCommand *existingRunnable = RunnableManager::getInstance().getCommand(data[0]);
                if (existingRunnable != NULL) {
                    TRACE("  > Runnable needs update.");
                    TRACE(
                            "  > Updated " + String(*existingRunnable));
                    // @todo implement the update.
                } else {
                    TRACE("  > Runnable needs create.");
                    commandToPatch->updateFromPayload(data);
                    RunnableManager::getInstance().addCommand(commandToPatch);
                    TRACE(
                            "  > Created " + String(*commandToPatch));
                }
            } else {
                // The data to use is the PATCH payload minus the two first bytes (CommandCode + ID)
                uint8_t *data = payload + 2;
                // In the case of a simple commandToPatch, we execute right away the commandToPatch.
                commandToPatch->executePayload(data);
            }
        }
};

REGISTER_COMMAND(CommandCode::PATCH, PatchCommand)

#endif  // ARDUINO_PATCH_COMMAND_H
