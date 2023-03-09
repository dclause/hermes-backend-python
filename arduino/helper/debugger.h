#ifndef ARDUINO_DEBUGGER_H
#define ARDUINO_DEBUGGER_H

#include <Arduino.h>

// Active debug: use 1, otherwise 0.
#define ACTIVATE_DEBUG 0
#define FORCE_SERIAL_DEBUG 1

#if ACTIVATE_DEBUG && FORCE_SERIAL_DEBUG && !defined(USE_SERIAL_PROTOCOL)
#define TRACE(X) Serial.println("# " + String(X))
#endif

// Defines the TRACE command.
#if ACTIVATE_DEBUG && !defined(TRACE)
#define TRACE(X) IO::debug(X)
#elif !defined(TRACE)
#define TRACE(X)
#endif

#endif // ARDUINO_DEBUGGER_H
