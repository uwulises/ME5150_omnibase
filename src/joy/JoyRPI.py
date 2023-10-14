import evdev
from evdev import InputDevice, categorize, ecodes
from ..serial_control.SerialControl import SerialControl
import time 
import numpy as np

# Process joystick input
def process_joystick(x_val=128,y_val=128,rs_x_val=128,rs_y_val=128):
    #round the values
    x_val=round(x_val)
    y_val=round(y_val)
    rs_x_val=round(rs_x_val)
    rs_y_val=round(rs_y_val)
    #create a vector with the joystick values
    joystick_vector_ls=(x_val,y_val)
    joystick_vector_rs=(rs_x_val,rs_y_val)
    # Match the vector to command
    switcher_ls = {
        (128,128): 'stop',
        (128,0): 'forward',
        (128,255): 'backward',
        (0,128): 'spin_left',
        (255,128): 'spin_right',
        }
    # Match the vector to command
    switcher_rs = {
        (128,128): 'stop',
        
        }
    func_ls = switcher_ls.get(joystick_vector_ls)
    func_rs = switcher_rs.get(joystick_vector_rs)
    if func_ls is None:
        func_ls = 'stop'
    elif func_rs is None:
        func_rs = 'stop'    
    base_comm.send_command(func_ls)
    #base_comm.send_command(func_rs)
    

def main():
    global x_axis
    global y_axis
    global rs_x_axis
    global rs_y_axis
    x_axis=0
    y_axis=0
    rs_x_axis=0
    rs_y_axis=0
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
            elif absevent.event.code == ecodes.ABS_Z:
                rs_x_axis = absevent.event.value
            elif absevent.event.code == ecodes.ABS_RZ:
                rs_y_axis = absevent.event.value
            process_joystick(x_axis,y_axis,rs_x_axis,rs_y_axis)
            print(x_axis,y_axis,rs_x_axis,rs_y_axis)

if __name__ == "__main__":
    base_comm = SerialControl()
    base_comm.open_serial()
    time.sleep(1)
    main()