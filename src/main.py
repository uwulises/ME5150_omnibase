import GetTrajectory
import SendVelocities
import numpy as np
import time

def main():
    dt = 0.5
    T_max = 10
    qf = [0.5, 0.2, 0.1]
    sv = SendVelocities.SendVelocities(port = "COM11")
    
    data = ""
    while "Dt" not in data:
        sv.send_dt(dt)
        data = sv.read()
        print('retorno dt:', data)
        time.sleep(0.1)
    
    sv.read_all()
    gt = GetTrajectory.GetTrajectory(qf, T_max, dt=dt)
    _, velocities_dt = gt.get_trajectory()
    print("Velocidades (dt):\n", velocities_dt)

    data = ""
    sv.send_velocities(velocities_dt)
    while "Traj" not in data:
        # sv.send_velocities(velocities_dt)
        data = sv.read()
        print('retorno:', data)
        time.sleep(0.1)

    sv.close()
    print("Done")

main()