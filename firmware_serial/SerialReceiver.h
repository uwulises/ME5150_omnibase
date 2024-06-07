// Encoder.h
#ifndef SERIAL_RECEIVER_H
#define SERIAL_RECEIVER_H

#include <Arduino.h> // Include this line to use Serial

class SerialReceiver {
    private:
        String msg;
        String action;

    public:
        SerialReceiver();
        float Vx = 0.0;
        float Vy = 0.0;
        float w = 0.0;
        void processMsg();
        void sendMsg();
        void receiveData();
        void getAction();
};

#endif // SERIAL_RECEIVER_H
