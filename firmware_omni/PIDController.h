// PIDController.h
#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

#include <Arduino.h>

class PIDController {
private:
    float prev_error;
    float integral;
    float Kp;
    float Ki;
    float Kd;
    float setpoint;
    unsigned long last_time;
    float outputMin;
    float outputMax;

public:
    PIDController(float Kp = 1.0,
                     float Ki = 0.0, 
                     float Kd = 0.0, 
                     float setpoint = 0.0, 
                     float outputMin = -255.0, 
                     float outputMax = 255.0);
    void setSetpoint(float setpointValue);
    float compute(float feedback);
    void debug(float error, float integral, float derivative, float output);
};

#endif
