#include <Arduino.h>
#include "helper/ioserial.h"
#include "debugger.h"
#include "commands.h"
#include "devices.h"

void setup() {
    IO::begin();

    // Clears out everything that might be left in the buffer.
    IO::clear();
}

void loop() {
    if (IO::available() > 0) {
        // Read incoming byte: this represents an order.
        CommandCode code = IO::read_command();

        // Make a command out of it.
        AbstractCommand *command = CommandFactory::getInstance().createCommand(code);
        TRACE(*command);

        // Execute the command
        command->receive();
        command->process();
    }
}
