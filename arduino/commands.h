#ifndef ARDUINO_COMMANDS_H
#define ARDUINO_COMMANDS_H

#include "commands/CommandCode.h"
#include "commands/AbstractCommand.h"
#include "commands/CommandFactory.h"

// /!\ All command includes must be listed here.
#include "commands/HandshakeCommand.h"
#include "commands/VoidCommand.h"
#include "commands/AckCommand.h"
#include "commands/BlinkCommand.h"
#include "commands/BooleanActionCommand.h"
#include "commands/PatchCommand.h"
#include "commands/ServoCommand.h"

#endif // ARDUINO_COMMANDS_H
