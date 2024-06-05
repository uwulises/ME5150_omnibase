import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from client.omnibase_robot_client import RobotClient
import time   

ip = '192.168.139.199' # "omni2.local"

robot = RobotClient(address=ip)

time.sleep(3)

robot.send_move_command('stop')
time.sleep(2)

robot.send_move_command('forward')
time.sleep(2)

robot.send_move_command('stop')
time.sleep(2)