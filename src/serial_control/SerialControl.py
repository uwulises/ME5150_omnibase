# __author__ = 'Ulises C.'
# __email__ = 'ulises.campodonico@ug.uchile.cl'

import serial
from serial import Serial
import time


class SerialControl:
    # Initialize the serial port
    def __init__(self, port="/dev/ttyUSB0"):
        self.port = port
        self.serial = None
        self.serial_port = ""

    # Open the serial port
    def open_serial(self):
        try:
            self.serial = Serial(self.port, 9600, timeout=1, write_timeout=0.2)
            print("The port is available")
            self.serial_port = "Open"
            time.sleep(2)
        except serial.serialutil.SerialException:
            print("The port is at use")
            self.serial.close()
            self.serial.open()

    # Send a command to the Arduino
    def send_command(self, command, cmd_vel=[0.0,0.0]):
        # Match case structure to send the right command to arduino
        vel= str(int(10*cmd_vel[0])).zfill(3) + str(int(10*cmd_vel[1])).zfill(3)
        switcher = {
            'forward': '1\n',
            'backward': '2\n',
            'spin_right': '3\n',
            'spin_left': '4\n',
            'lateral_right': '5\n',
            'lateral_left': '6\n',
            'diagonal_front_right': '7\n',
            'diagonal_front_left': '8\n',
            'diagonal_back_right': '9\n',
            'diagonal_back_left': '10\n',
            'cmd_vel': 'CMDVEL' + vel + '\n',
            'stop': 'STOP\n',
        }
        # Get the function from switcher dictionary
        func = switcher.get(command)
        if func is None:
            func = "STOP\n"
        # Execute the function
        self.serial.write(func.encode())

    def close_serial(self):
        time.sleep(0.2)
        self.serial.close()
        self.serial_port = "Close"
