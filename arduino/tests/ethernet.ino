#include <SPI.h>
#include <Ethernet.h>
#include <HardwareSerial.h>

#define IP 192, 168, 1, 20
#define PORT 5000
#define MAC { (byte)random(255), (byte)random(255), (byte)random(255), (byte)random(255), (byte)random(255), (byte)random(255) }
#define CS_PIN 10

EthernetUDP Udp;
uint8_t *buffer = new uint8_t[255];

void setup() {
    Ethernet.init(CS_PIN);
    byte mac[] = MAC;
    IPAddress ip(IP);
    Ethernet.begin(mac, ip);
    Udp.begin(PORT);
    Serial.begin(9600);
    Serial.println("Ready to test");
    pinMode(9, OUTPUT);
}

void loop() {
    if (Udp.parsePacket() > 0) {

        digitalWrite(9, HIGH);
        Serial.println("-------------------------------");
        Serial.println("Command code: " + String(Udp.read()));
        uint8_t available = Udp.available();
        Serial.println("Available: " + String(available));
        if (available >= 1) {
            uint8_t size = Udp.read();
            Serial.println("First byte: " + String(size));
            Udp.read(buffer, size);

            String payloadAsInts = "";
            for (uint8_t i = 0; i < size; i++) {
                payloadAsInts += String(buffer[i]) + " ";
            }
            Serial.println("Payload received: " + payloadAsInts);
        }
        digitalWrite(9, LOW);

        Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        Udp.write(11);
        Udp.endPacket();
    }
}
