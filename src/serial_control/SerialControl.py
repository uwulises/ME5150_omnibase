import serial
from serial import Serial
import time


class SerialControl:

    def __init__(self, port="/dev/ttyUSB0"):
        self.port = port
        self.serial = None

    def open_serial(self):
        try:
            self.serial = Serial(self.port, 9600, timeout=1, write_timeout=0.2)
            print("The port is available")
            serial_port = "Open"
            time.sleep(2)
        except serial.serialutil.SerialException:
            print("The port is at use")
            self.serial.close()
            self.serial.open()

    def close_serial(self):
        time.sleep(0.2)
        self.serial.close()

    def forward(self):
        self.serial.write('FW\n'.encode())

    def backward(self):
        self.serial.write('BW\n'.encode())

    def turn_right(self):
        self.serial.write('TR\n'.encode())

    def turn_left(self):
        self.serial.write('TL\n'.encode())

    def direct_left(self):
        self.serial.write('DL\n'.encode())

    def direct_right(self):
        self.serial.write('DR\n'.encode())
    
    def stop(self):
        self.serial.write('STOP\n'.encode())
   