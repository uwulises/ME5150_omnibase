#include "SerialReceiver.h"

SerialReceiver::SerialReceiver() {
}

void SerialReceiver::sendMsg() {
  Serial.print(1);
}

void SerialReceiver::processMsg() {
  int i = 0;
  action = "";
  while (msg[i] != ';') {
    action += msg[i];
    i++;
  }
  msg = msg.substring(i + 1);
}

void SerialReceiver::receiveData() {
  if (Serial.available() > 0) {
    msg = Serial.readStringUntil('\n');
    Serial.println(msg);
  }
  
}

String SerialReceiver::getMsg() {
  return msg;
}

void SerialReceiver::getAction() {
  int commaIndex1 = action.indexOf(',');
  int commaIndex2 = action.indexOf(',', commaIndex1 + 1);

  Vx = action.substring(0, commaIndex1).toFloat();
  Vy = action.substring(commaIndex1 + 1, commaIndex2).toFloat();
  w = action.substring(commaIndex2 + 1).toFloat();
  
  action = "";
}