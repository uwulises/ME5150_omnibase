import GetTrajectory
import SendVelocities
import numpy as np

def main():
    qf = [0.5, 0.2, 0.1]
    num_points = 10
    sv = SendVelocities.SendVelocities(port = "COM11")
    gt = GetTrajectory.GetTrajectory(qf, num_points)
    _, velocities = gt.get_trajectory()
    sv.send_velocities(velocities)
    print("Trajectory sent to the robot")
    for i in range(50):
        sv.read()
    
    sv.close()

main()