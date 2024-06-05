from flask import Flask
from threading import Thread
from SerialControl import SerialControl

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

@app.route('/move/<command>', methods=['GET'])
def move(command):
    drive_server.send_command(command)
    return "Command received: " + command

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,threaded=True)
