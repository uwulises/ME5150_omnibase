import numpy as np
import time

from rpiServer import RPIServer
from omniController import OmniController

server = RPIServer('0.0.0.0', 12345)
robot = OmniController()

while True:
    if server.client_conn is None:
        print("No client connected. Attempting to accept a new connection...")
        server.accept_connection()
    else:
        
        message = server.receive_message()
        if message:
            print("Received from PC:", message)
            server.send_confirmation()

            robot.calculate_vels(message)
            
            print('-Communication with RpiPico-')
            
            robot.send_data("DT")
            robot.send_data("DATA")
            
            print('-END Communication with RpiPico-')
            server.send_confirmation()
            
    time.sleep(0.1)
    print("Waiting for next message...")

robot.sv.close()
server.close_connection()
print("Done")
