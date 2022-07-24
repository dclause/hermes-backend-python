#include "helper/debugger.h"
#include "helper/ioserial.h"
#include "commands/commands.h"
#include <Arduino.h>

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
        if (command == NULL) {
            return;
        }

        TRACE(*command);

        // Execute the command
        command->process();

        IO::send_command(CommandCode::ACK);
    }
}
