import GetTrajectory
import SendVelocities
import numpy as np
import time

def main():
    dt = 0.5
    T_max = 5
    qf = [1, 0, 0]
    sv = SendVelocities.SendVelocities(port = "/dev/ttyACM0")
    jtraj_dt = GetTrajectory.GetTrajectory(qf, T_max, dt=dt)
    data = ""
    while "OK1" not in data:
        sv.send_dt(dt)
        data = sv.read()
        if len(data)>1:
            print('retorno:', data)
    _, velocities_dt = jtraj_dt.get_trajectory()
    # print("Velocidades (dt):\n", velocities_dt)
    sv.send_velocities(velocities_dt)
    while "OK2" not in data:
        data = sv.read()
        if len(data)>1:
            print('retorno:', data)
    print("NEXT POINT")
    qf = [0, 1, 0]

    jtraj_dt = GetTrajectory.GetTrajectory(qf, T_max, dt=dt)
    _, velocities_dt = jtraj_dt.get_trajectory()
    sv.send_velocities(velocities_dt)
    while "lal" not in data:
        data = sv.read()
        if len(data)>1:
            print('retorno:', data)
    

    sv.close()
    print("Done")

main()