// Encoder.h
#ifndef ENCODER_H
#define ENCODER_H

#include <Arduino.h> // Include this line to use Serial

struct Encoder {
    int pinA;
    int pinB;
    float wheelRadius;
    float velocity;
    volatile int position;
    int old_position;
    int lastAState;

    Encoder(int a, int b);
    void updateA();
    void updateB();
};

#endif // ENCODER_H
