import evdev
from evdev import InputDevice, categorize, ecodes
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
import time 

global base_comm
global previous_x_value
global previous_y_value
previous_x_value = 0
previous_y_value = 0

def process_joystick(x_val,y_val):

    if  x_val != previous_x_value:
        base_comm.forward() if x_val>0 else base_comm.backward()
    elif y_val != previous_y_value:
        base_comm.lateral_right() if y_val>0 else base_comm.lateral_left()
    
    previous_x_value = x_val
    previous_y_value = y_val

def main():
    
    # Find Xbox wireless controller
    gamepad = None
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)
    for device in devices:
        if "X-Box" in device.name:
            gamepad = device
            break

    # Process gamepad input
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            x_axis=0
            y_axis=0 
            if absevent.event.code == ecodes.ABS_X:
                x_axis = absevent.event.value / 32767.0
            elif absevent.event.code == ecodes.ABS_Y:
                y_axis = absevent.event.value / 32767.0
            process_joystick(x_axis,y_axis)

if __name__ == "__main__":
    base_comm = SerialControl(port="/dev/ttyACM0")
    base_comm.open_serial()
    time.sleep(1)
    main()