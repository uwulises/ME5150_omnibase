#include <Arduino.h>
#include "Encoder.h"
#include "PIDController.h"


/* TODO:
- Detectar cuando el encoder no está midiendo bien -> 
      Si se le entrega una vel por x tiempo, aproximar cuando debería ser (orden de magnitud) y alertar.
*/

#define QUARTER_PI 0.7853981633974483

#define M1_I1 5
#define M1_I2 6
#define M1_A 0
#define M1_B 1

#define M2_I1 4
#define M2_I2 3
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

const int NUM_ENCODERS = 4;
const int motors[NUM_ENCODERS][2] = {
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

int dt = 100;      // Periodo de actualización velocidad, en milisegundos
int dt_pid = 200;  // Periodo de actualización PID, en milisegundos
unsigned long t1_mot = 0;
unsigned long t1_pid = 0;

/* Parametros omni*/
const int l = 75;  // Mitad de la distancia entre las ruedas delanteras y traseras, e izquierdas y derechas, en mm
const int r = 27;  // Radio de las ruedas, en mm
const int lxy = sqrt(2) * l;

volatile long motorPos[] = { 0, 0, 0, 0 };
volatile long motorPrevPos[] = { 0, 0, 0, 0 };

float motorSpeed[] = { 0.0, 0.0, 0.0, 0.0 };
float controlSpeed[NUM_ENCODERS];

const int encoder_resolution = 2500;                // encoder steps per revolution
const int rad2enc = encoder_resolution / (2 * PI);  // encoder steps per radian 397

const int max_pwm = 255;                         // PWM
const int max_w_rads = 20;                       // rads/s o 0.5 m/s
const int max_w_encoder = max_w_rads * rad2enc;  // encoder steps per second
const int min_w_encoder = -max_w_encoder;        // encoder steps per second

// const float enc2pwm = max_pwm / float(max_w_encoder);  // PWM per encoder step

PIDController pid_controllers[NUM_ENCODERS] = {
  PIDController(0.01, 0.0001, 0.0),
  PIDController(0.01, 0.0001, 0.0),
  PIDController(0.01, 0.0001, 0.0),
  PIDController(0.01, 0.0001, 0.0),
};

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

  Serial.begin(115200);
  while (!Serial) {
    ; // Esperar a que se inicie la conexión serial
  }
}

void omni_IK(float Vx, float Vy, float w) {
  /* Set linear and angular velocity for the robot.
    @param linealVelocityX   linear velocity on the x axis, in m/s
    @param linealVelocityY   linear velocity on the y axis, in m/s
    @param angularVelocity   angular velocity, in rad/s
  */
  float w1 = (Vx + Vy + (lxy / 1000.0) * w) * 1000.0 / r;   // rads/sec
  float w2 = -(Vx - Vy - (lxy / 1000.0) * w) * 1000.0 / r;  // rads/sec
  float w3 = (Vx - Vy + (lxy / 1000.0) * w) * 1000.0 / r;   // rads/sec
  float w4 = -(Vx + Vy - (lxy / 1000.0) * w) * 1000.0 / r;  // rads/sec
  // Serial.print("w1:");
  // Serial.print(w1);
  // Serial.print("\t w2:");
  // Serial.print(w2);
  // Serial.print("\t w3:");
  // Serial.print(w3);
  // Serial.print("\t w4:");
  // Serial.println(w4);

  pid_controllers[0].setSetpoint(w1 * rad2enc);  // steps per sec
  pid_controllers[1].setSetpoint(w2 * rad2enc);  // steps per sec
  pid_controllers[2].setSetpoint(w3 * rad2enc);  // steps per sec
  pid_controllers[3].setSetpoint(w4 * rad2enc);  // steps per sec

  // Serial.print("w1:");
  // Serial.print(w1*rad2enc);
  // Serial.print("\t w2:");
  // Serial.print(w2*rad2enc);
  // Serial.print("\t w3:");
  // Serial.print(w3*rad2enc);
  // Serial.print("\t w4:");
  // Serial.println(w4*rad2enc);
}

bool withinTolerance(float signals[]) {
  // Function to check if all control signals are within a tolerance
  const float tolerance = 3;
  for (int i = 0; i < NUM_ENCODERS; i++) {
    if (abs(signals[i]) > tolerance) {
      return false;
    }
  }
  return true;
}

void apply_PID() {
  if (millis() - t1_pid >= dt_pid) {  //} && !withinTolerance(controlSpeed)) {
    t1_pid = millis();
    for (int i = 0; i < NUM_ENCODERS; i++) {
      controlSpeed[i] = pid_controllers[i].compute(motorSpeed[i]);
      set_motor_vel(i, controlSpeed[i]);
    }
  }
}

void set_motor_vel(int motor, int pwm) {  // vel: steps per sec
  /* Set velocity on a motor.
    @param motor  motor index number
    @param pwm    velocity and direction for the motor, -255 to 255
  */
  int IN1_PIN = motors[motor][0];
  int IN2_PIN = motors[motor][1];
  if (pwm < 0) {  // reverse speeds
    analogWrite(IN1_PIN, -pwm);
    digitalWrite(IN2_PIN, LOW);

  } else {  // stop or forward
    digitalWrite(IN1_PIN, LOW);
    analogWrite(IN2_PIN, pwm);
  }
}


void updateSpeed() {
  if (millis() - t1_mot >= dt) {
    t1_mot = millis();

    for (int i = 0; i < NUM_ENCODERS; i++) {
      motorPos[i] = encoders[i].position;
      motorSpeed[i] = (motorPos[i] - motorPrevPos[i]) / (dt / 1000.0);
      motorPrevPos[i] = motorPos[i];
    }
    for (int i = 0; i < NUM_ENCODERS; i++) {
      if (abs(motorSpeed[i]) < 150) {
        motorSpeed[i] = 0;
      }
    }
  }
}

void receiveData() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    Serial.print("Recibido: ");
    Serial.println(message);
  }
}

void loop(void) {
  
  updateSpeed();
  omni_IK(-0.4, 0, 0);  // en metros y rads/seg, Vx hacia adelante
  apply_PID();
  // Mostrar vel real
  // Serial.print("M1: ");
  // Serial.print(motorSpeed[0]);
  // Serial.print("\tM2: ");
  // Serial.print(motorSpeed[1]);
  // Serial.print("\tM3: ");
  // Serial.print(motorSpeed[2]);
  // Serial.print("\tM4: ");
  // Serial.println(motorSpeed[3]);
}
