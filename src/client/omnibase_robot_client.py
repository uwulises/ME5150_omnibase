import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "/RTC"))
from .RTC.WebRTC import WebRTCController
import socket

class RobotClient:

    def __init__(self, address, port=5000, portVideo=8080):
        self.address = address
        self.driver_port = port
        self.url = f'http://{self.address}:{self.driver_port}'
        self.connected = False
        self.webRTCUser = WebRTCController(self.address)
        self.driver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectWebRTC(self):
        self.webRTCUser.connect()

    def closeWebRTC(self):
        self.webRTCUser.close()
        

    def showVideo(self, process= lambda frame : (frame, None)):
        self.webRTCUser.showVideo(process)
    
    def stopVideo(self):
        self.webRTCUser.stopVideo()
    

    def get_frame(self):
        return self.webRTCUser.getFrame()

    def send_move_command(self,command):
        try:
            response = requests.get(f'{self.url}/move/{command}')
            if response.status_code == 200:
                print(f'Successfully sent command: {command}')
            else:
                print(f'Failed to send command: {command}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')