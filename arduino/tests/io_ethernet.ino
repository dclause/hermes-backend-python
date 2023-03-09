#define IP 192, 168, 1, 20
#define PORT 5000
#define MAC { (byte)random(255), (byte)random(255), (byte)random(255), (byte)random(255), (byte)random(255), (byte)random(255) }
#define CS_PIN 10

#include "../helper/debugger.h"
#include "../protocols/io_ethernet.h"
#include <Ethernet.h>
#include <EthernetUdp.h>


EthernetUDP Udp;
uint8_t *buffer = new uint8_t[255];

void setup() {
    IO::begin();
    Serial.begin(9600);
    TRACE("Ready to test");
}

void loop() {
    if (IO::parsePacket() > 0) {
        TRACE("-------------------------------");

        TRACE("Command code: " + String(IO::read_command()));
        uint8_t available = IO::available();
        TRACE("Available: " + String(available));

        IO::wait_for_bytes(1);
        IO::read_bytes(buffer, 1);
        uint8_t size = buffer[0];
        TRACE("First byte: " + String(size));

        IO::wait_for_bytes(size);
        IO::read_bytes(buffer, size);
        String payloadAsInts = "";
        for (uint8_t i = 0; i < size; i++) {
            payloadAsInts += String(buffer[i]) + " ";
        }
        TRACE("Payload received: " + payloadAsInts);

        IO::send_command(11);
    }
}
