#include <Arduino.h>
#include "helper/map.h"

#define BAUDRATE 9600

void setup() {
    Serial.begin(BAUDRATE);

    KeyValueMap<String, String> map;
    map.add("foo", "bar");
    map.add("foo2", "bar2");
    map.add("foo3", "bar3");
    Serial.println(map);

    Serial.println("-----------------------------");
    String result = map.getValue("foo2");
    Serial.println("foo2 should be bar2: " + result);

    Serial.println("-----------------------------");
    String result2 = map.get(1)->value;         // Positions start at 0 !
    Serial.println("2nd element should be bar2: " + result2);

    Serial.println("-----------------------------");
    int result3 = map.getPosition("foo2") + 1;      // Positions start at 0 !
    Serial.println("foo3 key is the 2nd element: " + String(result3));

    Serial.println("-----------------------------");
    Serial.println("Let's remove foo2");
    map.remove("foo2");
    Serial.println(map);

    Serial.println("Remaining map size should be 2 : " + String(map.count()));
}

void loop() {}