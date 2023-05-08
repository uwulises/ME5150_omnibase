
import pygame

pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
x_last = 0 #initial value for x_val
y_last = 0 #intitial value for y_val

while True:
    try:
        pygame.event.get()
        x_axis = round(joystick.get_axis(0))
        y_axis = -round(joystick.get_axis(1))
                
        if (x_axis != x_last or y_axis != y_last):
            x_last=x_axis
            y_last=y_axis

    except KeyboardInterrupt:
        print("DESCONECTADO")
        break