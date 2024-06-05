from flask import Flask
from threading import Thread
from SerialControl import SerialControl
import socket

app = Flask(__name__)

class DriveServer:
    def __init__(self):
        self.base_comm = SerialControl()
        self.base_comm.open_serial()

    def send_command(self, data):
        # This method will now run in a separate thread to avoid blocking the Flask server
        t = Thread(target=self.base_comm.send_command, args=(data,))
        t.start()

drive_server = DriveServer()

# UDP server configuration
UDP_IP = "0.0.0.0"
UDP_PORT = 5001
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def udp_listener():
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        command = data.decode('utf-8')
        drive_server.send_command(command)

# Start the UDP listener in a separate thread
udp_thread = Thread(target=udp_listener)
udp_thread.start()

@app.route('/move/<command>', methods=['GET'])
def move(command):
    # For demonstration purposes, you can still handle HTTP requests and forward commands to SerialControl
    drive_server.send_command(command)
    return "Command received: " + command

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
