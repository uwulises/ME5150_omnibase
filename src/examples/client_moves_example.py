import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient, RobotDriverClient
import time   

robot = RobotClient(address="omni.local")
driver = RobotDriverClient(address="omni.local")

driver.send_move_command('forward')
time.sleep(5)
driver.send_move_command('backward')
time.sleep(5)
driver.send_move_command('stop')
