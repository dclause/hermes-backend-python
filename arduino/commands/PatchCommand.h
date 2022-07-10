#ifndef ARDUINO_PATCH_COMMAND_H
#define ARDUINO_PATCH_COMMAND_H

#include <Arduino.h>

#include "../debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"

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
            TRACE((String) F("  > Received data: ") + String((char *) this->payload_));
            uint8_t deviceCode = this->payload_[0];
        }
};

REGISTER_COMMAND(CommandCode::PATCH, PatchCommand)

#endif  // ARDUINO_PATCH_COMMAND_H
