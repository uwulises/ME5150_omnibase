import GetTrajectory
import SendVelocities
import numpy as np

def main():
    qf = [0.1, 0.2, 0.1]
    num_points = 100
    sv = SendVelocities.SendVelocities()
    gt = GetTrajectory.GetTrajectory(qf, num_points)

    _, velocities = gt.get_trajectory()
    
    sv.send_velocities(velocities)
    print("Trajectory sent to the robot")
    sv.close()