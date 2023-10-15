import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient
import time   
import cv2
import numpy as np

def onlygray(frame):

  gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  return gray, None

robot = RobotClient("omni.local")

robot.showVideo(process= onlygray)
time.sleep(10)
robot.closeWebRTC()