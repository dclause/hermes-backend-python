#ifndef ARDUINO_HANDSHAKE_COMMAND_H
#define ARDUINO_HANDSHAKE_COMMAND_H

#include <Arduino.h>
#include "../helper/debugger.h"
#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"
#include "../helper/ioserial.h"

/**
 * HANDSHAKE Command: performs the HANDSHAKE sequence.
 *
 * This sequence is done on the initiative of the remote master and must complete to be considered done.
 *
 * @see CommandCode::HANDSHAKE
 */
class HandshakeCommand : public AbstractCommand {
    COMMAND_DECLARATION
    public:

        HandshakeCommand() : AbstractCommand(1) {}

        String getName() const { return "Handshake"; }

        void executePayload(uint8_t *payload) {
            TRACE("-----------");
            TRACE("Process HANDSHAKE command:");

            for (uint8_t i = 0; i < payload[0]; ++i) {
                if (IO::wait_for_bytes(1)) {
                    CommandCode code = IO::read_command();
                    if (code != CommandCode::PATCH) {
                        TRACE("ERROR in received code: " + String((uint8_t) code));
                        return;
                    }
                    AbstractCommand *command = CommandFactory::getInstance().createCommand(code);
                    command->process();
                }
            }
            IO::send_command(CommandCode::ACK);
        }
};

REGISTER_COMMAND(CommandCode::HANDSHAKE, HandshakeCommand)

#endif // ARDUINO_HANDSHAKE_COMMAND_H
