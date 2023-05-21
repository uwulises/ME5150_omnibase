// https://www.elecrow.com/wiki/index.php?title=Arduino_Motor/Stepper/Servo_Shield
#include <AFMotor.h>
#include <Servo.h>

String inputString = "";
bool stringComplete = false;

AF_DCMotor motor1(1); //BL
AF_DCMotor motor2(2); //BR
AF_DCMotor motor3(3); //FL
AF_DCMotor motor4(4); //FR

void setup()
{
  //softspeed();
  Serial.begin(9600);
  delay(1000);
  Serial.println("----");
  Serial.println("READY");
  Serial.println("----");
  delay(200);
  motor1.setSpeed(200);
  motor2.setSpeed(200);
  motor3.setSpeed(200);
  motor4.setSpeed(200);
}

void serialEvent()
{
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void serialReading() {
  if (stringComplete) {
    Serial.println(inputString);
    if (inputString == "FW\n") {
      FW();
    }
    if (inputString == "BW\n") {
      BW();
    }
    if (inputString == "SR\n") {
      SR();
    }
    if (inputString == "SL\n") {
      SL();
    }
    if (inputString == "LR\n") {
      LR();
    }
    if (inputString == "LL\n") {
      LL();
    }
    if (inputString == "DFR\n") {
      DFR();
    }
    if (inputString == "DFL\n") {
      DFL();
    }
    if (inputString == "DBR\n") {
      DBR();
    }
    if (inputString == "DBL\n") {
      DBL();
    }
    if (inputString == "STOP\n") {
      STOP();
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

void FW() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}
void BW() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}
void SL() { //spin antihorario
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}
void SR() {//spin horario
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}
void DFL() { //Diagonal frente izquierda
  motor1.run(FORWARD);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(FORWARD);
}
void DFR() { //Diagonal frente derecha
  motor1.run(RELEASE);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(RELEASE);
}
void DBL() { //Diagonal atras izquierda
  motor1.run(RELEASE);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(RELEASE);
}
void DBR() { //Diagonal atras derecha
  motor1.run(BACKWARD);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(BACKWARD);
}

void LR() { //lateral derecha
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}
void LL() {//lateral izquierda
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}
void STOP() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void loop() {
  serialReading();
}
