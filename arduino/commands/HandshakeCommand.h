#ifndef ARDUINO_HANDSHAKE_COMMAND_H
#define ARDUINO_HANDSHAKE_COMMAND_H

#include <Arduino.h>
#include "../debugger.h"
#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"

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
        String getName() const { return "Handshake"; }

        void process() {
            TRACE((String) F("Start Handshake"));
            Serial.write((uint8_t) CommandCode::CONNECTED);
        }
};

REGISTER_COMMAND(CommandCode::HANDSHAKE, HandshakeCommand)

#endif // ARDUINO_HANDSHAKE_COMMAND_H
