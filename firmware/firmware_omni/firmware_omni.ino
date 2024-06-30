#include <Arduino.h>

#include "Encoder.h"
#include "PIDController.h"
#include "SerialReceiver.h"
#include "parameters.h"


// Variables
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

volatile long motorPos[] = { 0, 0, 0, 0 };
volatile long motorPrevPos[] = { 0, 0, 0, 0 };

float motorSpeed[] = { 0.0, 0.0, 0.0, 0.0 };
float controlSpeed[NUM_ENCODERS];

PIDController pid_controllers[NUM_ENCODERS] = {
  PIDController(0.00001, 0.0000000001, 0.0),
  PIDController(0.00001, 0.0000000001, 0.0),
  PIDController(0.00001, 0.0000000001, 0.0),
  PIDController(0.00001, 0.0000000001, 0.0),
};

// IGNORE
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


// Variables seriales

SerialReceiver serialR;
float dt = 0;
String msg = "";
String msg1 = "";
String act = "";
long unsigned int dt_ready = 3000;
long unsigned int last_ready = 0;
int state = 0;

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
    ;  // Esperar a que el puerto serie esté listo
  }
  delay(3000);  // Espera inicial para dar tiempo a la conexión serie
  state = 1;    // Inicia en el estado 1
}

void loop() {

  // Si se corta la comunicación serie, detener los motores
  if (!Serial) {
    state = 0;
  } else {  // Si hay comunicación serie, actualizar la velocidad de los motores
    updateSpeed();
  }

  switch (state) {

    // Estado 0: Si no hay comunicación serie, detener los motores
    case 0:
      if (!Serial) {
        stop_motors();  // Detener los motores
        state = 0;      // Mantener en estado 0 si no hay comunicación serie
      } else {          // Si hay comunicación serie, pasar al estado 1
        dt = 0;
        msg = "";
        state = 1;  // Pasar al estado 1 si hay comunicación serie
      }
      break;

    // Estado 1: Obtener dt del monitor serie
    case 1:
      if (millis() - last_ready >= dt_ready) {
        last_ready = millis();
        serialR.sendMsg("DT");
      }

      serialR.receiveData();
      dt = serialR.getMsg().toFloat();

      if (dt != 0) {

        serialR.sendMsg("OK1");
        state = 2;  // Pasar al estado 2 después de enviar "Dt"
        serialR.setMsg();
      }
      break;

    // Estado 2: Recibir trayectoria a traves del monitor serie
    case 2:
      stop_motors();
      if (millis() - last_ready >= dt_ready) {  // Si ha pasado dt_ready ms
        last_ready = millis();
        serialR.sendMsg("DATA");                // Enviar "waiting data"
      }
      serialR.receiveData();
      msg = serialR.getMsg();
      if (msg != "") {
        state = 3;  // Pasar al estado 3 si se recibe algún mensaje
      }
      break;

    // Estado 3: Obtener la siguiente acción para el robot
    case 3:
      // Procesar el mensaje del monitor serie
      serialR.processMsg();
      serialR.splitAction();
      last_ready = millis();

      // Pasar al estado 4 después de procesar el mensaje
      state = 4;
      break;

    // Estado 4: Mover el robot
    case 4:
      // Si ha pasado menos que dt
      if (millis() - last_ready < dt * 1000) {
        omni_IK(serialR.Vx, serialR.Vy, serialR.w);  // en metros y rads/seg, Vx hacia adelante
        apply_PID();
        break;
      }
      msg = serialR.getMsg();

      if (msg == "") {
        serialR.sendMsg("OK2");
        state = 1;  // Volver al estado 2 si no hay mensaje

      } else {
        state = 3;  // Volver al estado 3 si hay mensaje
      }
      break;

    default:
      state = 0;
      break;
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

  pid_controllers[0].setSetpoint(w1 * rad2enc);  // steps per sec
  pid_controllers[1].setSetpoint(w2 * rad2enc);  // steps per sec
  pid_controllers[2].setSetpoint(w3 * rad2enc);  // steps per sec
  pid_controllers[3].setSetpoint(w4 * rad2enc);  // steps per sec
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
  // if (millis() - t1_pid >= dt_pid) {  //} && !withinTolerance(controlSpeed)) {
  // t1_pid = millis();
  for (int i = 0; i < NUM_ENCODERS; i++) {
    controlSpeed[i] = pid_controllers[i].compute(motorSpeed[i]);
    set_motor_vel(i, controlSpeed[i]);
  }
  // }
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

void stop_motors() {
  /* Set all motors to stop.
  */
  for (int i = 0; i < NUM_ENCODERS; i++) {
    set_motor_vel(i, 0);
  }
}

void updateSpeed() {
  if (millis() - t1_mot >= dt_vel) {
    t1_mot = millis();

    for (int i = 0; i < NUM_ENCODERS; i++) {
      motorPos[i] = encoders[i].position;
      motorSpeed[i] = (motorPos[i] - motorPrevPos[i]) / (dt_vel / 1000.0);
      motorPrevPos[i] = motorPos[i];
    }
    for (int i = 0; i < NUM_ENCODERS; i++) {
      if (abs(motorSpeed[i]) < 150) {
        motorSpeed[i] = 0;
      }
    }
  }
}
