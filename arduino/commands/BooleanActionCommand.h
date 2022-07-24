#ifndef ARDUINO_DIGITAL_WRITE_COMMAND_H
#define ARDUINO_DIGITAL_WRITE_COMMAND_H

#include <Arduino.h>

#include "../debugger.h"
#include "AbstractCommand.h"
#include "CommandCode.h"
#include "CommandFactory.h"
#include "../devices/AbstractDevice.h"
#include "../devices/DeviceManager.h"

/**
 * DIGITAL_WRITE Command: toggle a digital pin write.
 *
 * @see CommandCode::DIGITAL_WRITE
 */
class BooleanActionCommand : public AbstractCommand {
    COMMAND_DECLARATION

    public:

        BooleanActionCommand() : AbstractCommand(2) {}

        String getName() const { return "DigitalWrite"; }

        void executePayload(uint8_t *payload) {
            TRACE((String) F("Process DigitalWrite command."));

            uint8_t pin = payload[0];
            uint8_t value = payload[1];

            TRACE((String) F("  > Set pin ") + (String) pin + F(" to: ") + (String) value);

            pinMode(pin, OUTPUT);
            digitalWrite(pin, value);
        }
};

REGISTER_COMMAND(CommandCode::BOOLEAN_ACTION, BooleanActionCommand)

#endif  // ARDUINO_DIGITAL_WRITE_COMMAND_H
