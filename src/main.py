from GetTrajectory import GetTrajectory
from SendVelocities import SendVelocities
import numpy as np
import time
from RPIServer import RPIServer


class OmniController:
    def __init__(self, port = "/dev/ttyACM0"):
        self.sv = SendVelocities(port = port)
            
    def split_message(self, message):
        assert isinstance(message, str), "Message must be a string."       
        x, y, o, dt, t_max = message.split(',')
        x = float(x.split(':')[-1])
        y = float(y.split(':')[-1])
        o = float(o.split(':')[-1])
        dt = float(dt.split(':')[-1])
        t_max = float(t_max.split(':')[-1])
        return x, y, o, dt, t_max

    def get_vels(self, qf, T_max, dt):
        gt = GetTrajectory(qf, T_max, dt=dt)
        _, velocities_dt = gt.get_trajectory()
        return velocities_dt

def main():
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

                x, y, o, dt, t_max = robot.split_message(message)
                qf = [x, y, o]
                
                print('-Communication with RpiPico-')

                # Send dt to Arduino
                data = ""
                while "OK1" not in data:
                    robot.sv.send_dt(dt)
                    data = robot.sv.read()
                    print('Retorno:', data)
                    time.sleep(0.1)
                
                vels = robot.get_vels(qf, t_max, dt)

                # Send velocities to Arduino
                while "OK2" not in data:
                    robot.sv.send_velocities(vels)
                    data = robot.sv.read()
                    print('Retorno:', data)
                    time.sleep(0.1)

                print('-END Communication with RpiPico-')
                server.send_confirmation()
                
                
        time.sleep(0.1)
        
    robot.sv.close()
    server.close_connection()
    

    # sv.read_all()
    # gt = GetTrajectory(qf, T_max, dt=dt)
    # _, velocities_dt = gt.get_trajectory()
    # print("Velocidades (dt):\n", velocities_dt)

    # data = ""
    # sv.send_velocities(velocities_dt)
    # while "Traj" not in data:
    #     # sv.send_velocities(velocities_dt)
    #     data = sv.read()
    #     print('retorno:', data)
    #     time.sleep(0.1)

    # sv.close()
    # print("Done")

main()