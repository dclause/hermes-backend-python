#ifndef ARDUINO_ONOFF_COMMAND_H
#define ARDUINO_ONOFF_COMMAND_H

#include <Arduino.h>

#include "../debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"

/**
 * ON_OFF Command: toggle a digital pin ON/OFF.
 *
 * @see CommandCode::ON_OFF
 */
class OnOffCommand : public AbstractCommand {
    COMMAND_DECLARATION

    public:

        OnOffCommand() : AbstractCommand(2) {}

        String getName() const { return "OnOff"; }

        void process() {
            TRACE((String) F("Process OnOff command."));

            uint8_t deviceId = this->payload_[0];
            uint8_t value = this->payload_[1];
            TRACE((String) F("  > Requested device ") + (String) deviceId + F(" to be set to: ") + (String) value);

            // @todo use the devices (when handshake is implemented)
            pinMode(13, OUTPUT);
            digitalWrite(13, value);
        }
};

REGISTER_COMMAND(CommandCode::ON_OFF, OnOffCommand)

#endif  // ARDUINO_ONOFF_COMMAND_H
