#ifndef ARDUINO_DEBUGGER_H
#define ARDUINO_DEBUGGER_H

#include <Arduino.h>

// Active debug: use 1, otherwise 0.
#define ACTIVATE_DEBUG 0

// Defines the TRACE command.
#if ACTIVATE_DEBUG
#define TRACE(X) IO::debug(X)
#else
#define TRACE(X)
#endif

#endif // ARDUINO_DEBUGGER_H
