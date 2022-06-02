#ifndef ARDUINO_BLINK_COMMAND_H
#define ARDUINO_BLINK_COMMAND_H

#include <Arduino.h>
#include "../debugger.h"
#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"

/**
 * BLINK Command: blinks a led.
 *
 * @see CommandCode::BLINK
 */
class BlinkCommand : public AbstractCommand {
    COMMAND_DECLARATION
    public:
        String getName() const { return "Blink"; }

        // @todo blinks according to parameters.
        void process() {
            TRACE((String) F("Start Blink"));
            pinMode(13, OUTPUT);

            for (int i = 0; i < 3; i++) {
                digitalWrite(13, HIGH);
                delay(200);
                digitalWrite(13, LOW);
                delay(200);
            }
        }
};

REGISTER_COMMAND(CommandCode::BLINK, BlinkCommand)

#endif // ARDUINO_BLINK_COMMAND_H
