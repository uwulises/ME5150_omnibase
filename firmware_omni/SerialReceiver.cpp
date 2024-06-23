#include "SerialReceiver.h"

SerialReceiver::SerialReceiver() : serial2(16, 17) {
  // Inicializa serial2 en el constructor
  serial2.begin(115200);
}


void SerialReceiver::sendMsg(const String &msg) {
  f_msg = msg + "\n";
  serial2.write(f_msg.c_str());
}

void SerialReceiver::setMsg(const String &msg) {
  receive_msg = msg;
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
  while (serial2.available() > 0) {
    receive_msg = serial2.read(); //receive_msg += (char)serial2.read();
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
  while (serial2.available() > 0) {
    serial2.read();
  }
}

String SerialReceiver::getAction() {
  return action;
}

String SerialReceiver::getMsg() {
  return receive_msg;
}

bool SerialReceiver::available() {
  return serial2.available() > 0;
}