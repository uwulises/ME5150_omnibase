import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient
import time   

robot = RobotClient("omni.local")

robot.send_move_command('forward')
time.sleep(5)
robot.send_move_command('backward')
