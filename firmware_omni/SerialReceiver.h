#ifndef SERIAL_RECEIVER_H
#define SERIAL_RECEIVER_H

#include <Arduino.h>

class SerialReceiver {
private:
  String action = "";
  String receive_msg = "";
  String f_msg = "";
  SerialPIO serial2;

public:
  SerialReceiver();
  float Vx = 0.0;
  float Vy = 0.0;
  float w = 0.0;
  void sendMsg(const String &msg = "1");
  void setMsg(const String &msg = "");
  void receiveData();
  void processMsg();
  void splitAction();
  void clearSerialBuffer();
  bool available();
  String getMsg();
  String getAction();
};

#endif
