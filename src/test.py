import GetTrajectory
import SendVelocities
import numpy as np
import time

def main():
    dt = 0.5
    T_max = 10
    sv = SendVelocities.SendVelocities(port = "/dev/serial0")
    data = ""
    while "Dt" not in data:
        data = sv.read()
        print('retorno:', data)
        time.sleep(0.1)
    
    sv.close()
    print("Done")

main()