import time
import serial

class SendVelocities:
    # Initialize the serial port
    def __init__(self, port="/dev/serial0"):
        self.port = port
        self.serial = None
        self.open_serial()

    # Open the serial port
    def open_serial(self):
        try:
            self.serial = serial.Serial(
                port = self.port,
                baudrate = 115200,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 1
            )
            print("The port is available")
            time.sleep(2)
        except serial.serialutil.SerialException:
            print("The port is at use")
            self.serial.close()
            self.serial.open()
        
        
    def send_velocities(self, velocities: list):
        assert velocities.shape[1] == 3, "Path must have 3 columns"
        if self.serial is None:
            print('Serial port is not open')
            return

        msg = ''
        for vels in velocities:
            
            msg += self.format_vel(vels)
        self.serial.write(msg.encode())
        print("Path sent")

    def format_vel(self, vels):
        # solo 3 decimales
        vx = "{:.3f}".format(vels[0])
        vy = "{:.3f}".format(vels[1])
        w = "{:.3f}".format(vels[2])
        return f"{vx},{vy},{w};"

    def read(self):
        data = self.serial.readline()
        decoded_data = data.decode()
        return decoded_data


    def close(self):
        self.serial.close()

def main():
    velocities = np.random.rand(10, 3)
    sv = SendVelocities()
    sv.send_velocities(velocities)
    sv.close()

if __name__ == "__main__": 
    main()