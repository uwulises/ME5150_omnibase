import requests
import json
from .webRTC import WebRTCController
from .videoShow import VideoShow

class RobotClient:

    def __init__(self, address, port=5000, portVideo=8080):
        self.address = address
        self.port = port
        self.base_url = f"http://{address}:{port}"
        self.connected = False
        self.session = requests.Session()
        self.webRTCUser = WebRTCController(self.address)

    def connect(self):
        if self.connected:
            print("already connected :)")
            return

        url = f"{self.base_url}/connect"
        response = self.session.get(url)
        if response.status_code == 200:
            self.connected = True
            print(response.text)
    
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
        
    def home(self):
        self.set_joints(q0=self.HOME_Q0, q1=self.HOME_Q1, q2=self.HOME_Q2)