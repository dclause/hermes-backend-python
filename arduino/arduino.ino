#include <Arduino.h>
#include "debugger.h"
#include "commands.h"
#include "devices.h"

#define BAUDRATE 115200

void setup() {
    Serial.begin(BAUDRATE);
    TRACE("Board started");

    // Clears out everything that might be left in the buffer.
    while (Serial.available() > 0) {
        Serial.read();
    }
}

void loop() {
    if (Serial.available() > 0) {
        // Read incoming byte: this represents an order.
        auto code = Serial.read();
        TRACE((String) F("Command code received: ") + (uint8_t) code);

        // Make a command out of it.
        auto command = CommandFactory::getInstance().createCommand((CommandCode) code);
        TRACE(*command);

        // Execute the command
        command->process();
    }
}
