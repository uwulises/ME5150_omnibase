
#include "Arduino.h"
#include "SerialReceiver.h"

SerialReceiver::SerialReceiver() {
    
}

SerialReceiver::processMsg() {
    int i = 0;
    action = "";
    while (msg[i] != ';') {
        action += msg[i];
        i++;
    }
    msg = msg.substring(i + 1);
}

SerialReceiver::sendMsg() {
    Serial.println("available");
}

SerialReceiver::receiveData() {
    if (Serial.available() > 0) {
        msg = Serial.readStringUntil('\n');
    }
}

SerialReceiver::getAction() {
    int commaIndex1 = action.indexOf(',');
    int commaIndex2 = action.indexOf(',', commaIndex1 + 1);

    Vx = action.substring(0, commaIndex1).toFloat();
    Vy = action.substring(commaIndex1 + 1, commaIndex2).toFloat();
    W = action.substring(commaIndex2 + 1).toFloat();

    action = "";
}