from flask import Flask, request
from SerialControl import SerialControl

app = Flask(__name)

class DriveServer:
    def __init__(self):
        self.base_comm = SerialControl()
        self.base_comm.open_serial()

    def send_command(self, data):
        self.base_comm.send_command(data)

@app.route('/move/<command>', methods=['GET'])
def move(command):
    drive_server.send_command(command)
    return "Command received: " + command

if __name__ == "__main__":
    drive_server = DriveServer()
    app.run(host='0.0.0.0', port=5000)