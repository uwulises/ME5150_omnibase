#include <Arduino.h>
#include "Encoder.h"
#include "PIDController.h"

#define QUARTER_PI 0.7853981633974483

#define M1_I1 4
#define M1_I2 3
#define M1_A 0
#define M1_B 1
#define M2_I1 5
#define M2_I2 6
#define M2_A 15
#define M2_B 14
#define M3_I1 10
#define M3_I2 9
#define M3_A 20
#define M3_B 21
#define M4_I1 11
#define M4_I2 12
#define M4_A 19
#define M4_B 18

const int motors[4][2] = {
  { M1_I1, M1_I2 },
  { M2_I1, M2_I2 },
  { M3_I1, M3_I2 },
  { M4_I1, M4_I2 }
};

Encoder encoders[] = {
  { M1_A, M1_B },
  { M2_A, M2_B },
  { M3_A, M3_B },
  { M4_A, M4_B }
};

int dt = 100;  // Periodo de actualización velocidad, en milisegundos
unsigned long previousMillis = 0;
unsigned long currentMillis = 0;

/* Parametros miniomni*/
const int R = 75;  // Distancia desde el centro de robot al centro de las ruedas, en mm
const int r = 25;  // Radio de las ruedas, en mm

volatile long motorPos[] = { 0, 0, 0, 0 };
volatile long motorPrevPos[] = { 0, 0, 0, 0 };

float motorSpeed[] = { 0.0, 0.0, 0.0, 0.0 };
float controlSpeed[sizeof(encoders)];

const int encoder_resolution = 2500;                  // encoder steps per revolution
const int rad2enc = encoder_resolution / (2 * PI);  // encoder steps per radian 397

const int max_pwm = 255;                         // PWM
const int max_w_rads = 20;                       // rads/s o 0.5 m/s
const int max_w_encoder = max_w_rads * rad2enc;  // encoder steps per second

const float enc2pwm = max_pwm / max_w_encoder;  // PWM per encoder step

PIDController pid_controllers[sizeof(encoders)];

void isrA0() {
  encoders[0].updateA();
}
void isrB0() {
  encoders[0].updateB();
}
void isrA1() {
  encoders[1].updateA();
}
void isrB1() {
  encoders[1].updateB();
}
void isrA2() {
  encoders[2].updateA();
}
void isrB2() {
  encoders[2].updateB();
}
void isrA3() {
  encoders[3].updateA();
}
void isrB3() {
  encoders[3].updateB();
}

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(motors[i][0], OUTPUT);
    pinMode(motors[i][1], OUTPUT);
    digitalWrite(motors[i][0], LOW);
    digitalWrite(motors[i][1], LOW);
  }
  attachInterrupt(digitalPinToInterrupt(encoders[0].pinA), isrA0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[0].pinB), isrB0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[1].pinA), isrA1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[1].pinB), isrB1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[2].pinA), isrA2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[2].pinB), isrB2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[3].pinA), isrA3, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoders[3].pinB), isrB3, CHANGE);

  for (int i = 0; i < sizeof(encoders); ++i) {
    pid_controllers[i] = PIDController(1, 0.5, 0.0, 0.0);  // Adjust parameters as needed
  }

  Serial.begin(115200);
}
/* Set the current on a motor channel using PWM and directional logic.
  @param pwm      PWM duty cycle ranging from -255 full reverse to 255 full forward
  @param IN1_PIN  pin number xIN1 for the given channel
  @param IN2_PIN  pin number xIN2 for the given channel
*/
void set_motor_pwm(int pwm, int IN1_PIN, int IN2_PIN) {
  if (pwm < 0) {  // reverse speeds
    analogWrite(IN1_PIN, -pwm);
    digitalWrite(IN2_PIN, LOW);

  } else {  // stop or forward
    digitalWrite(IN1_PIN, LOW);
    analogWrite(IN2_PIN, pwm);
  }
}

/* Set velocity on a motor.
   @param motor  motor index number
   @param pwm    velocity and direction for the motor, -255 to 255
*/
void set_motor_vel(int motor, int vel_enc) {  // vel: steps per sec
  int pwm = vel_enc * enc2pwm;

  set_motor_pwm(pwm, motors[motor][0], motors[motor][1]);
}

/* Set linear and angular velocity for the robot.
   @param linealVelocityX   linear velocity on the x axis, in m/s
   @param linealVelocityY   linear velocity on the y axis, in m/s
   @param angularVelocity   angular velocity, not sure of the measurement for this one
*/
void miniomni_IK(float Vx, float Vy, float w) {
  float w1 = (-sin(QUARTER_PI) * Vx + cos(QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000) ;          // rads/sec
  float w2 = (-sin(3 * QUARTER_PI) * Vx + cos(3 * QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000) ;  // rads/sec
  float w3 = (-sin(5 * QUARTER_PI) * Vx + cos(5 * QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000) ;  // rads/sec
  float w4 = (-sin(7 * QUARTER_PI) * Vx + cos(7 * QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000) ;  // rads/sec

  pid_controllers[0].setSetpoint(w1 * rad2enc);  // steps per sec
  pid_controllers[1].setSetpoint(w2 * rad2enc);  // steps per sec
  pid_controllers[2].setSetpoint(w3 * rad2enc);  // steps per sec
  pid_controllers[3].setSetpoint(w4 * rad2enc);  // steps per sec

  unsigned long startTime = millis();  // Record the start time

  // Loop until 1 second has passed or control signals are within a tolerance
  while (millis() - startTime < 1000 && !withinTolerance(controlSpeed)) {
    Serial.println("dentro del loop de miniomni_IK");
    withinTolerance(controlSpeed);
    for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
      controlSpeed[i] = pid_controllers[i].compute(motorSpeed[i]);  // Set control signals
      set_motor_vel(i, controlSpeed[i]);                            // Change the motor speed
    }
  }
}

void updateSpeed() {
  currentMillis = millis();
  if (currentMillis - previousMillis >= dt) {
    previousMillis = currentMillis;

    for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
      motorPos[i] = encoders[i].position;
      motorSpeed[i] = (motorPos[i] - motorPrevPos[i]) / (dt / 1000.0);
      motorPrevPos[i] = motorPos[i];
    }
  }
}

// Function to check if all control signals are within a tolerance
bool withinTolerance(float signals[]) {
  const float tolerance = 3;
  for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
    if (abs(signals[i]) > tolerance) {
      return false;
    }
  }
  return true;
}

void loop(void) {
  updateSpeed();
  miniomni_IK(0, 1, 0); // en metros y rads/seg, Vy hacia adelante
  delay(50);
}
