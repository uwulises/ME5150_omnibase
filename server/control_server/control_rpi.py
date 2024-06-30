import numpy as np
import time

from rpiServer import RPIServer
from omniController import OmniController

server = RPIServer('0.0.0.0', 12345)
robot = OmniController()
dt_print = 2
last_time = time.time()

while True:
    if not server.is_client_connected():
        print("No client connected. Attempting to accept a new connection...")
        server.accept_connection()
    else:     
        print("Receiving message...")       
        message = server.receive_message()
        if message:
            print("Received from PC:", message)
            
            print("Calculando velocidades...")
            robot.calculate_vels(message)
            
            print('-Communication with RpiPico-')
            
            robot.send_data("DT")
            robot.send_data("DATA")
            
            print('-END Communication with RpiPico-')
            server.send_confirmation()
    time.sleep(0.1)
    if time.time() > last_time + dt_print:
        print("Waiting for next message...")
        last_time = time.time()
        
robot.sv.close()
server.close_connection()
print("Done")
