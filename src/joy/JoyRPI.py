import evdev
from evdev import InputDevice, categorize, ecodes
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
import time 

# Process joystick input
def process_joystick(x_val,y_val):

    x_val=round(x_val)
    y_val=round(y_val)

    if (y_val==1 and x_val==0):
        base_comm.send_command('forward')

    elif (y_val==-1 and x_val==0):
        base_comm.send_command('backward')

    elif (x_val==-1 and y_val==0):
        base_comm.send_command('lateral_right')

    elif (x_val==1 and y_val==0):
        base_comm.send_command('lateral_left')

    else:
        base_comm.send_command('stop')

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
                x_axis = absevent.event.value / 32767.0
            elif absevent.event.code == ecodes.ABS_Y:
                y_axis = absevent.event.value / 32767.0
            process_joystick(x_axis,y_axis)

if __name__ == "__main__":
    base_comm = SerialControl()
    base_comm.open_serial()
    time.sleep(1)
    main()