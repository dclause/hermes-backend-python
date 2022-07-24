#include "helper/debugger.h"
#include "helper/ioserial.h"
#include "helper/commands.h"
#include <Arduino.h>

void setup() {
    IO::begin();
    IO::clear();
}

void loop() {
    Commands::receive_and_process_next_command();
    Commands::update_all_runnables();
}