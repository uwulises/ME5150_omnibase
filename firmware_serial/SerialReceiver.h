#ifndef SERIAL_RECEIVER_H
#define SERIAL_RECEIVER_H

#include <Arduino.h>  // Include this line to use Serial

class SerialReceiver {
private:
  String action = "";
  String msg = "";

public:
  SerialReceiver();
  float Vx = 0.0;
  float Vy = 0.0;
  float w = 0.0;
  void sendMsg();
  void receiveData();
  void processMsg();
  void getAction();
  String getMsg();
};

#endif
