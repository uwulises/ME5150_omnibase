import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient, RobotDriverClient
import time   

robot = RobotClient(address="omni.local")
driver = RobotDriverClient(address="omni.local")
time.sleep(1)
driver.send_move_command('forward')
driver.send_move_command('stop')
driver.send_move_command('backward')
driver.send_move_command('stop')
