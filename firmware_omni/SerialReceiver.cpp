#include "SerialReceiver.h"

SerialReceiver::SerialReceiver() {
}

void SerialReceiver::sendMsg(const String &msg) {
  Serial.println(msg);  // Usar println para indicar el fin del mensaje
}

void SerialReceiver::setMsg(const String &msg) {
  receive_msg = "";
}

void SerialReceiver::processMsg() {
  int i = 0;
  action = "";
  while (i < receive_msg.length() && receive_msg[i] != ';') {
    action += receive_msg[i];
    i++;
  }
  if (i < receive_msg.length()) {
    receive_msg = receive_msg.substring(i + 1);
  } else {
    receive_msg = "";
  }
}

void SerialReceiver::receiveData() {
  while (Serial.available() > 0) {
    receive_msg = Serial.readStringUntil('\n');
  }
}

void SerialReceiver::splitAction() {
  // Buscar los índices de las comas en el mensaje
  int commaIndex = action.indexOf(',');
  int commaIndex2 = action.indexOf(',', commaIndex + 1);
  int commaIndex3 = action.length();

  // Extraer los valores de las subcadenas
  Vx = action.substring(0, commaIndex).toFloat();
  Vy = action.substring(commaIndex + 1, commaIndex2).toFloat();
  w = action.substring(commaIndex2 + 1, commaIndex3).toFloat();

  // Limpiar la acción después de procesarla
  action = "";
}

void SerialReceiver::clearSerialBuffer() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}

String SerialReceiver::getAction() {
  return action;
}

String SerialReceiver::getMsg() {
  return receive_msg;
}
