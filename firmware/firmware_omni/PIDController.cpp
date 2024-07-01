#include "Arduino.h"
#include "PIDController.h"

PIDController::PIDController(float Kp, float Ki, float Kd, float setpoint, float outputMin, float outputMax) {
    this->Kp = Kp;
    this->Ki = Ki;
    this->Kd = Kd;
    this->setpoint = setpoint;
    this->prev_error = 0;
    this->integral = 0;
    this->last_time = millis();
    this->outputMin = outputMin;
    this->outputMax = outputMax;
}

float PIDController::compute(float feedback){
    unsigned long current_time = millis();
    float delta_time = (current_time - last_time) / 1000.0;  // Convert to seconds
    last_time = current_time;

    float error = setpoint - feedback;
    integral += error * delta_time;
    float derivative = (error - prev_error) / delta_time;
    float cal = Kp * error + Ki * integral + Kd * derivative;
    prev_error = error;

    int output = constrain(cal, outputMin, outputMax);
    // Serial.print(setpoint);
    // Serial.print('\t');
    // Serial.print(feedback);
    // Serial.print('\t');
    // Serial.print(cal);
    // Serial.print('\t');
    // Serial.println(output);
    //debug(error, integral, derivative, output);
    return output;
}

void PIDController::setSetpoint(float setpointValue) {
    setpoint = setpointValue;
    integral = 0;
    prev_error = 0;
    // last_time = millis();
}

void PIDController::debug(float error, float integral, float derivative, float output) {
    Serial.print("Error: ");
    Serial.print(error);
    Serial.print(" Integral: ");
    Serial.print(integral);
    Serial.print(" Derivative: ");
    Serial.print(derivative);
    Serial.print(" Output: ");
    Serial.println(output);
}
