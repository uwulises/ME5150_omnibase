#include "SerialReceiver.h"

SerialReceiver serialR;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
}
void loop() {

  if (serialR.getMsg() == "") {
    serialR.receiveData();
  } else {
    serialR.processMsg();  // action = 'Vx,Vy,W'
    serialR.getAction();
  }
}