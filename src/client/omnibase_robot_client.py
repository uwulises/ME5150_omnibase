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
    
    def connect_driver_socket(self):
        try:
            self.driver_socket.connect((self.address, self.driver_port))
        except Exception as e:
            print("Error connecting to the server:", str(e))

    def send_command(self, command):

        self.driver_socket.send(command.encode())
        response = self.driver_socket.recv(1024).decode()
        print(response)
        return response

    def close_driver(self):
        self.driver_socket.close()