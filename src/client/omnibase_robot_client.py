import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "/RTC"))
from .RTC.WebRTC import WebRTCController
import time
class RobotClient:

    def __init__(self, address="omni.local"):
        self.address = address
        self.connected = False
        self.webRTCUser = WebRTCController(self.address)
        self.url = f'http://{self.address}:5000'
        
    def connectWebRTC(self):
        self.webRTCUser.connect()

    def closeWebRTC(self):
        self.webRTCUser.close()
        
    def showVideo(self):
        self.webRTCUser.showVideo()
    
    def stopVideo(self):
        self.webRTCUser.stopVideo()
    
    def get_frame(self):
        return self.webRTCUser.getFrame()
    
    def send_move_command(self,command):
        try:
            start_time = time.time()
            response = requests.get(f'{self.url}/move/{command}', timeout=(0.05))
            if response.status_code == 200:
                print(f'Successfully sent command: {command}')
                time_elapsed = time.time() - start_time
                print(time_elapsed)
            else:
                print(f'Failed to send command: {command}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')