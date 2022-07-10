#ifndef ARDUINO_ACK_COMMAND_H
#define ARDUINO_ACK_COMMAND_H

#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"

/**
 * ACK Command: acknowledges.
 *
 * ACK are usually sent from the slave to the master to acknowledge reception and
 * process of a command.
 *
 * @see arduino loop()
 * @see CommandCode::ACK
 */
class AckCommand : public AbstractCommand {
    COMMAND_DECLARATION
    public:
        String getName() const { return "ACK"; }

        void send() {
            IO::send_command(CommandCode::ACK);
        }

        void process() {}
};

REGISTER_COMMAND(CommandCode::ACK, AckCommand)

#endif // ARDUINO_ACK_COMMAND_H
