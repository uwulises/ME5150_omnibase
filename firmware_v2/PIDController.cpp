#include "Arduino.h"
#include "PIDController.h"

PIDController::PIDController(float Kp, float Ki, float Kd, float setpoint){
    this->Kp = Kp;
    this->Ki = Ki;
    this->Kd = Kd;
    this->setpoint = setpoint;
    this->prev_error = 0;
    this->integral = 0;
}
float PIDController::compute(float feedback){
    float error = setpoint - feedback;
    integral += error;
    float derivative = error - prev_error;
    float output = Kp * error + Ki * integral + Kd * derivative;
    prev_error = error;
    Serial.print("Error: ");
    Serial.print(error);
    Serial.print(" Integral: ");
    Serial.print(integral);
    Serial.print(" Derivative: ");
    Serial.print(derivative);
    Serial.print(" Output: ");
    Serial.println(output);
    return output;
}

void PIDController::setSetpoint(float setpointValue) {
    setpoint = setpointValue;
}
