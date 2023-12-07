import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "/RTC"))
from .RTC.WebRTC import WebRTCController
import socket
import time
class RobotClient:

    def __init__(self, address="omni.local"):
        self.address = address
        self.connected = False
        self.webRTCUser = WebRTCController(self.address)
        

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



class RobotDriverClient:
    def __init__(self, address="omni.local", port=5000):
        self.driver_port = port
        self.address = address
        self.url = f'http://{self.address}:{self.driver_port}'

    def send_move_command(self,command):
        try:
            start_time = time.time()
            response = requests.get(f'{self.url}/move/{command}', timeout=0.3)    
            if response.status_code == 200:
                print(f'Successfully sent command: {command}')
                time_elapsed = time.time() - start_time
                print(time_elapsed)
            else:
                print(f'Failed to send command: {command}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')