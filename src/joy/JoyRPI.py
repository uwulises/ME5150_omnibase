import evdev
from evdev import InputDevice, categorize, ecodes
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
import time 

global x_axis
global y_axis

base_comm = SerialControl("COM4")
base_comm.open_serial()
time.sleep(2)

def call_moves(x=0,y=0,a=0, b=0):

    base_comm.forward() if y>0 else base_comm.backward()
    time.sleep(0.5)


def process_joystick(joystick=[0,0]):
    """
    Process joystick values and perform actions.
    Modify this function according to your requirements.
    """
    x_axis = joystick[0]
    y_axis = joystick[1]

    # Example action based on joystick values
    if x_axis < -0.5:
        print("Left")
    elif x_axis > 0.5:
        print("Right")
    elif y_axis < -0.5:
        print("Up")
        call_moves(y=y_axis)
    elif y_axis > 0.5:
        print("Down")
        call_moves(y=y_axis)
    else:
        print("Neutral")

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

    if gamepad is None:
        print("No Xbox wireless controller found")
        return

    print("Xbox wireless controller found:", gamepad.name)

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
            joystick_values = [x_axis, y_axis]
            process_joystick(joystick_values)

if __name__ == "__main__":
    main()