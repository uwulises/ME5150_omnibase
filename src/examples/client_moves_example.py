import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient
import time   

robot = RobotClient(address="omni.local")
time.sleep(1)
robot.send_move_command('forward')
robot.send_move_command('stop')
robot.send_move_command('backward')
robot.send_move_command('stop')
