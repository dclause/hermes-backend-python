#ifndef ARDUINO_COMMANDS_H
#define ARDUINO_COMMANDS_H

#include "CommandCode.h"
#include "AbstractCommand.h"
#include "CommandFactory.h"

// /!\ All command includes must be listed here.
#include "AckCommand.h"
#include "BooleanActionCommand.h"
#include "HandshakeCommand.h"
#include "PatchCommand.h"
#include "ServoCommand.h"
#include "VoidCommand.h"

#endif // ARDUINO_COMMANDS_H
