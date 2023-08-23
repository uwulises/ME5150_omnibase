// https://www.elecrow.com/wiki/index.php?title=Arduino_Motor/Stepper/Servo_Shield
#include <AFMotor.h>

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
    //Serial.println(inputString);
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
    //take the 6 first characters of the string
    //and compare it with "CMDVEL" 
    if (inputString.substring(0, 6) == "CMDVEL") {
      //take the 7th character of the string
      int axial_speed = inputString.substring(6, 9).toInt();
      int angular_speed = inputString.substring(9, 12).toInt();
      // divide by 10.0 and convert to float to get the decimal point
      float axial_speed_f = axial_speed / 10.0;
      float angular_speed_f = angular_speed / 10.0;
      //call cmd vel function
      cmd_vel(axial_speed_f, angular_speed_f);
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

//call motors function to move the robot, takes an array of 4 floats as argument
void motors(float w[4]) {
}

// cmd_vel function that takes two floats as arguments of mecanum wheeled robot
void cmd_vel(float vx, float vy) {
  // Te distance between the center of the robot and the wheel D=0.1m and the radius of the wheel R=0.05m
  float D = 0.15;
  float R = 0.05;
  int w_max = 400;
  //create a v array to store the speed of each wheel
  float w[4];
  w[0] = (vx - vy)/R;
  w[1] = (vx + vy)/R;
  w[2] = (vx + vy)/R;
  w[3] = (vx - vy)/R;
  // transform v from m/s to rpm, to 0-255 pwm given that the maximun speed of the motor is 400rpm
  for (int i = 0; i < 4; i++) {
    w[i] = w[i] * 60 / (2 * PI * R);
    w[i] = w[i] * 255 / w_max;
  }

   //call a function that takes the v array as argument and move the wheels.
  motors(w);

  
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
