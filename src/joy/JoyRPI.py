from evdev import InputDevice, categorize, ecodes

def process_joystick(joystick):
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
    elif y_axis > 0.5:
        print("Down")
    else:
        print("Neutral")

def main():
    # Find Xbox wireless controller
    gamepad = None
    devices = [InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "Xbox" in device.name:
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
            if absevent.event.code == ecodes.ABS_X:
                x_axis = absevent.event.value / 32767.0
            elif absevent.event.code == ecodes.ABS_Y:
                y_axis = absevent.event.value / 32767.0
            joystick_values = (x_axis, y_axis)
            process_joystick(joystick_values)

if __name__ == "__main__":
    main()