import GetTrajectory
import SendVelocities
import numpy as np

def main():
    dt = 0.5
    T_max = 10
    qf = [0.5, 0.2, 0.1]
    sv = SendVelocities.SendVelocities(port = "/dev/serial0")

    gt = GetTrajectory.GetTrajectory(qf, T_max, dt=dt)
    _, velocities_dt = gt.get_trajectory()
    print("Velocidades (dt):\n", velocities_dt)

    sv.send_velocities(velocities_dt)
    print("Trajectory sent to the robot")
    for i in range(50):
        sv.read()
    
    sv.close()

main()