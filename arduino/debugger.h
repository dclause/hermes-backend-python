#ifndef ARDUINO_DEBUGGER_H
#define ARDUINO_DEBUGGER_H

#include <Arduino.h>

// Active debug: use 1.
#define ACTIVATE_DEBUG 1

// Defines the TRACE command.
#if ACTIVATE_DEBUG
#define TRACE(X) trace(X)
#else
#define TRACE(X) ;
#endif

/**
 * Outputs the data on the serial monitor.
 *
 * @details
 * All debug strings must be wrapped as follow:
 *  - DEBUG byte (@see Order.h) to indicate the other hand of the Serial communication to avoid this.
 *  - a [SPACE] byte (value 32)
 *  - an arbitrarily long string
 *  - a [EndOfLine] byte (value 10)
 *
 * For instance if debug param info is "Hello World", the sent data are : "# Hello World"
 * # is the byte 32 registered as the DEBUG command which will be received and interpreted both
 * on server and arduino side as pure DEBUG.
 *
 * @param info
 */
void trace(const String &info) {
    Serial.println("# " + info);
}

#endif // ARDUINO_DEBUGGER_H
