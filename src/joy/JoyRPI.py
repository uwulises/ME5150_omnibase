import evdev
from evdev import InputDevice, categorize, ecodes
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
import time 
import numpy as np

# Process joystick input
def process_joystick(x_val,y_val):

    x_val=round(x_val)
    y_val=round(y_val)
    #create a vector with the joystick values
    joystick_vector=(x_val,y_val)

    # Match the vector to command
    switcher = {
        (128,128): 'stop',
        (255,0): 'forward',
        (0,255): 'backward'}

    func = switcher.get(joystick_vector, lambda: "Invalid command")
    base_comm.send_command(func)
    

def main():
    global x_axis
    global y_axis
    x_axis=0
    y_axis=0
    # Find Xbox wireless controller
    gamepad = None
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)
    for device in devices:
        if "X-Box" in device.name:
            gamepad = device
            break
        elif "ShanWan" in device.name:
            gamepad = device
            break

    # Process gamepad input
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            if absevent.event.code == ecodes.ABS_X:
                x_axis = absevent.event.value
            elif absevent.event.code == ecodes.ABS_Y:
                y_axis = absevent.event.value
            process_joystick(x_axis,y_axis)
            print(x_axis,y_axis)

if __name__ == "__main__":
    base_comm = SerialControl()
    base_comm.open_serial()
    time.sleep(1)
    main()