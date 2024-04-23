#include <Arduino.h>
#include "Encoder.h"

// Define motor pins
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
  {M1_I1, M1_I2},
  {M2_I1, M2_I2},
  {M3_I1, M3_I2},
  {M4_I1, M4_I2}
};


// Global array of encoders
Encoder encoders[] = {
    {0, 1},  // Encoder for Motor 1
    {15, 14},  // Encoder for Motor 2
    {20, 21},  // Encoder for Motor 3
    {19, 18}   // Encoder for Motor 4
};

void isrA0() {encoders[0].updateA(); }
void isrB0() {encoders[0].updateB(); }
void isrA1() {encoders[1].updateA(); }
void isrB1() {encoders[1].updateB(); }
void isrA2() {encoders[2].updateA(); }
void isrB2() {encoders[2].updateB(); }
void isrA3() {encoders[3].updateA(); }
void isrB3() {encoders[3].updateB(); }

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

}
/* Set the current on a motor channel using PWM and directional logic.
 *@param pwm      PWM duty cycle ranging from -255 full reverse to 255 full forward
 *@param IN1_PIN  pin number xIN1 for the given channel
 *@param IN2_PIN  pin number xIN2 for the given channel 
 */
void set_motor_pwm(int pwm, int IN1_PIN, int IN2_PIN)
{
  if (pwm < 0) {  // reverse speeds
    analogWrite(IN1_PIN, -pwm);
    digitalWrite(IN2_PIN, LOW);

  } else { // stop or forward
    digitalWrite(IN1_PIN, LOW);
    analogWrite(IN2_PIN, pwm);
  }
}

/* Set velocity on a motor.
 * @param motor  indice del motor
 * @param pwm    velocidad y sentido del motor, -255 to 255
 */
void set_motor_vel(int motor, int pwm) {
  set_motor_pwm(pwm, motors[motor][0], motors[motor][1]);

  Serial.print("Set motor ");
  Serial.print(motor);
  Serial.print(" PWM = ");
  Serial.println(pwm);
}

/*Simple primitive for the motion sequence to set a speed and wait for an interval.
 * @param motor    indice del motor
 * @param pwm      velocidad y sentido del motor, -255 to 255
 * @param duration delay in milliseconds (optional)
 */
void spin_and_wait(int motor, int pwm, int duration=500) {
  set_motor_vel(motor, pwm);
  delay(duration);
}

void loop(void)
{ 
  spin_and_wait(1, 150, 1000);
  for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
          Serial.print("Encoder ");
          Serial.print(i);
          Serial.print(" Position: ");
          Serial.println(encoders[i].position);
    }
  
  spin_and_wait(1, 0, 2000);

  for (int i = 0; i < sizeof(encoders) / sizeof(encoders[0]); i++) {
        Serial.print("Encoder ");
        Serial.print(i);
        Serial.print(" Position: ");
        Serial.println(encoders[i].position);
  }
  
}

