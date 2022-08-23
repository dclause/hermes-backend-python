#ifndef ARDUINO_COMMANDS_H
#define ARDUINO_COMMANDS_H

#include "ioserial.h"
#include "map.h"
#include "../commands/CommandCode.h"
#include "../commands/AbstractCommand.h"
#include "../commands/CommandFactory.h"
#include "../commands/RunnableManager.h"

// ! All command includes must be listed here.
#include "../commands/BooleanActionCommand.h"
#include "../commands/HandshakeCommand.h"
#include "../commands/PatchCommand.h"
#include "../commands/MutationCommand.h"
#include "../commands/ServoCommand.h"
#include "../commands/VoidCommand.h"

namespace Commands {

    /**
     * Read the next command in the IO buffer and process it.
     * Once done, an ACK is sent.
     */
    void receive_and_process_next_command() {
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

    /**
     * Loop over Runnable commands and update them.
     */
    void update_all_runnables() {
        KeyValuePair<uint8_t, AbstractCommand *> *node = RunnableManager::getInstance().getHead();
        while (node) {
            node->value->nextTick();
            node = node->next;
        }
    }

}  // namespace Commands

#endif // ARDUINO_COMMANDS_H
