#ifndef ARDUINO_VOID_COMMAND_H
#define ARDUINO_VOID_COMMAND_H

#include <HardwareSerial.h>
#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"

/**
 * VOID Command: does nothing !
 *
 * It's purpose is to let any none attributed CommandCode be mapped to a real command (this one) by the factory.
 * This ensures that factory always returns a real command that can be processed (and do nothing here).
 *
 * @see CommandCode::VOID
 */
class VoidCommand : public AbstractCommand {
    COMMAND_DECLARATION
    public:
        String getName() const { return "VOID"; }

        void process() {}
};

REGISTER_COMMAND(CommandCode::VOID, VoidCommand)

#endif // ARDUINO_VOID_COMMAND_H
