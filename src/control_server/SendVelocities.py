import time
import serial

class SendVelocities:
    # Initialize the serial port
    def __init__(self, port="/dev/serial0"):
        self.port = port
        self.serial = None
        self.open()

    # Open the serial port
    def open(self):
        try:
            self.serial = serial.Serial(
                port = self.port,
                baudrate = 115200,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 2
            )
            print("The port is available")
            time.sleep(2)
        except serial.serialutil.SerialException as e:
            print(f"Failed to open serial port: {e}")
            if self.serial:
                self.serial.close()
            raise
        
    def send_velocities(self, velocities: list):
        assert velocities.shape[1] == 3, "Path must have 3 columns"
        if self.serial is None:
            print('Serial port is not open')
            return

        msg = ''
        for vels in velocities:
            msg += self.format_vel(vels)
        self.send(msg)
        print("Path sent")

    def send_dt(self, dt):
        if self.serial is None:
            print('Serial port is not open')
            return
        msg = f"{dt}"
        self.send(msg)

    def format_vel(self, vels):
        # solo 3 decimales
        vx = "{:.4f}".format(vels[0])
        vy = "{:.4f}".format(vels[1])
        w = "{:.4f}".format(vels[2])
        return f"{vx},{vy},{w};"

    def read(self):
        data = self.serial.readline()
        decoded_data = data.decode().strip()
        return decoded_data

    def send(self, msg):
        self.serial.write(msg.encode())
    
    def read_all(self):
        data = self.serial.read_all()
        decoded_data = data.decode().strip()
        return decoded_data

    def close(self):
        if self.serial:
            self.serial.close()
            print("Serial port closed")

def main():
    velocities = np.random.rand(10, 3)
    sv = SendVelocities()
    sv.send_velocities(velocities)
    sv.close()

if __name__ == "__main__": 
    main()