from GetFrame import RobotClient
import time
import numpy as np

robot = RobotClient("192.168.166.233")
img = robot.get_frame()

print(img)

robot.closeWebRTC()