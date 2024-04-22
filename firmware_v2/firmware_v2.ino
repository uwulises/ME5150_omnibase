// Define motor pins
#define M1_I1 4
#define M1_I2 3
#define M2_I1 5
#define M2_I2 6
#define M3_I1 10
#define M3_I2 9
#define M4_I1 11
#define M4_I2 12

const int motors[4][2] = {
  {M1_I1, M1_I2},
  {M2_I1, M2_I2},
  {M3_I1, M3_I2},
  {M4_I1, M4_I2}
};

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(motors[i][0], OUTPUT);
    pinMode(motors[i][1], OUTPUT);
    digitalWrite(motors[i][0], LOW);
    digitalWrite(motors[i][1], LOW);
  }

  Serial.begin(9600);


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
void spin_and_wait(int motor, int pwm, int duration=500)
{
  set_motor_currents(motor, pwm);
  delay(duration);
}

void loop(void)
{ // Motor 1 a vel 150 por 1seg
  spin_and_wait(1, 150, 1000);
  // Motor 1 a vel -150 por 0.5 segs
  spin_and_wait(1, -150);

}

