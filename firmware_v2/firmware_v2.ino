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

const float R = 0.075;  // Distancia desde el centro de robot al centro de las ruedas, en m
const float r = 0.025;  // Radio de las ruedas, en m

volatile long motorPos[] = { 0, 0, 0, 0 };
volatile long motorPrevPos[] = { 0, 0, 0, 0 };

float motorSpeed[] = { 0.0, 0.0, 0.0, 0.0 };
float controlSpeed[sizeof(encoders)];

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
    pid_controllers[i] = PIDController(1.0, 0.0, 0.0, 0.0);  // Adjust parameters as needed
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
void set_motor_vel(int motor, int pwm) {
  set_motor_pwm(pwm, motors[motor][0], motors[motor][1]);

  Serial.print("Set motor ");
  Serial.print(motor);
  Serial.print(" PWM = ");
  Serial.println(pwm);
}

/* Set linear and angular velocity for the robot.
   @param linealVelocityX   linear velocity on the x axis, in m/s
   @param linealVelocityY   linear velocity on the y axis, in m/s
   @param angularVelocity   angular velocity, not sure of the measurement for this one
*/
void set_velocity(int Vx, int Vy, int w, int pwm = 255) {

  // Calculations for the target values:
  pid_controllers[0].setSetpoint(Vx + Vy + r * w);
  pid_controllers[1].setSetpoint(Vx - Vy - r * w);
  pid_controllers[2].setSetpoint(Vx - Vy + r * w);
  pid_controllers[3].setSetpoint(Vx + Vy - r * w);

  unsigned long startTime = millis();  // Record the start time

  // Loop until 1 second has passed or control signals are within a tolerance
  while (millis() - startTime < 3000 && !withinTolerance(controlSpeed)) {
    for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
      controlSpeed[i] = pid_controllers[i].compute(motorSpeed[i]);  // Set control signals
      set_motor_vel(i, controlSpeed[i]);                            // Change the motor speed
    }
  }
}

// Function to check if all control signals are within a tolerance
bool withinTolerance(float signals[]) {
  float tolerance = 0.1;  // Adjust this tolerance as needed
  for (int i = 0; i < sizeof(encoders); i++) {
    if (abs(signals[i]) > tolerance) {
      return false;  // If any signal is not within tolerance, return false
    }
  }
  return true;  // If all signals are within tolerance, return true
}

void miniomni_IK(int Vx, int Vy, int w) {
  float w1 = (-sin(QUARTER_PI) * Vx + cos(QUARTER_PI) * Vy + R * w) * 1 / r;
  float w2 = (-sin(3 * QUARTER_PI) * Vx + cos(3 * QUARTER_PI) * Vy + R * w) * 1 / r;
  float w3 = (-sin(5 * QUARTER_PI) * Vx + cos(5 * QUARTER_PI) * Vy + R * w) * 1 / r;
  float w4 = (-sin(7 * QUARTER_PI) * Vx + cos(7 * QUARTER_PI) * Vy + R * w) * 1 / r;

  pid_controllers[0].setSetpoint(w1);
  pid_controllers[1].setSetpoint(w2);
  pid_controllers[2].setSetpoint(w3);
  pid_controllers[3].setSetpoint(w4);

  unsigned long startTime = millis();  // Record the start time

  // Loop until 1 second has passed or control signals are within a tolerance
  while (millis() - startTime < 1000 && !withinTolerance(controlSpeed)) {
    for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
      controlSpeed[i] = pid_controllers[i].compute(motorSpeed[i]);  // Set control signals

      set_motor_vel(i, controlSpeed[i]);                            // Change the motor speed
    }
  }

  Serial.print(w1);
  Serial.print(w2);
  Serial.print(w3);
  Serial.print(w4);
  Serial.println("-------");
}

void updateSpeed() {
  currentMillis = millis();
  if (currentMillis - previousMillis >= dt) {
    previousMillis = currentMillis;

    for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
      motorPos[i] = encoders[i].position;
      motorSpeed[i] = (motorPos[i] - motorPrevPos[i]) / (dt / 1000.0);
      motorPrevPos[i] = motorPos[i];

      /* Imprimir las velocidades en el monitor serie
      Serial.print("Motor ");
      Serial.print(i + 1);
      Serial.print(" Speed: ");
      Serial.println(motorSpeed[i]);*/
    }
  }
}


void loop(void) {
  updateSpeed();
  miniomni_IK(0, 1, 0);
  delay(500);
}
