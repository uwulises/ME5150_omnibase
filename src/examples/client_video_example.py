import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient
import time   
import cv2
import numpy as np

ip = "192.168.139.21" # or "omni2.local"

robot = RobotClient(ip)
print('Starting video...')
robot.showVideo()
time.sleep(3)
print('Stopping video...')
robot.stopVideo()
robot.closeWebRTC()

# while True:
#   alo = robot.get_frame()
#   cv2.imshow("alo", alo)
#   if cv2.waitKey(1) & 0xFF == ord('q'):
#     break