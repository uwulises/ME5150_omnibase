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
        switcher = {
            'forward': 'FW\n',
            'backward': 'BW\n',
            'spin_right': 'SR\n',
            'spin_left': 'SL\n',
            'lateral_right': 'LR\n',
            'lateral_left': 'LL\n',
            'diagonal_front_right': 'DFR\n',
            'diagonal_front_left': 'DFL\n',
            'diagonal_back_right': 'DBR\n',
            'diagonal_back_left': 'DBL\n',
            'cmd_vel': 'CMDVEL' + str(int(10*cmd_vel[0])).zfill(3) + str(int(10*cmd_vel[1])).zfill(3) + '\n',
            'stop': 'STOP\n'
        }
        # Get the function from switcher dictionary
        func = switcher.get(command, lambda: "Invalid command")
        # Execute the function
        self.serial.write(func.encode())

    def close_serial(self):
        time.sleep(0.2)
        self.serial.close()
        self.serial_port = "Close"
