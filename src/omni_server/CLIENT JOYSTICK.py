import threading
import asyncio
import websockets
import base64
import cv2
import numpy as np
import socket
import pygame
import time


class VideoReceiver:
    def __init__(self, server_url):
        self.server_url = server_url

    async def receive_video(self):
        async with websockets.connect(self.server_url, ping_interval=None) as websocket:
            try:
                while True:
                    # Receive the frame from the server
                    encoded_image = await websocket.recv()
                   
                    # Decode the base64 encoded frame
                    decoded_image = base64.b64decode(encoded_image)

                    # Convert the frame to NumPy array
                    np_arr = np.frombuffer(decoded_image, dtype=np.uint8)

                    # Decode the image array using OpenCV
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    #probar un filtro de imagen 
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # Display the frame
                    cv2.imshow('Video Stream', frame)
                    if cv2.waitKey(1) == 27:
                        break

            finally:
                cv2.destroyAllWindows()


    def start_receiving(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.receive_video())

class RemoteControl:

    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            # Connect to the server
            self.client_socket.connect((self.server_address, self.server_port))
            print('Connected to the server.')
            pygame.init()
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            
            while True:
                # Valor mínimo para considerar como acción
                action_threshold = 0.2

                # Tiempo mínimo entre acciones (en segundos)
                min_time_between_actions = 0.03
                last_action_time = time.time() - min_time_between_actions

                # Bandera para controlar si se ha realizado una acción de tope
                action_triggered = False

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                    # Leer valores de las palancas (ejes) del joystick
                    x_axis = joystick.get_axis(2)
                    y_axis = joystick.get_axis(3)
                    x_axis_rot = joystick.get_axis(0)
                    boton_stop = joystick.get_button(2)
                    boton_exit = joystick.get_button(3)
                
                    # Tiempo actual
                    current_time = time.time()

                    # Acción de tope (solo se imprime una vez)
                    if y_axis == 1 and not action_triggered:
                        print("Mover hacia adelante (tope)")
                        action_triggered = True

                    # Movimientos diagonales y en los ejes X e Y
                    elif abs(x_axis) > action_threshold or abs(y_axis) > action_threshold or abs(x_axis_rot) > action_threshold or boton_stop == True or boton_exit == True:
                        if current_time - last_action_time > min_time_between_actions:
                            if abs(x_axis) > action_threshold and abs(y_axis)> action_threshold:
                                if x_axis > 0 and y_axis > 0:
                                    command = "diagonal_back_right"
                                elif x_axis > 0 and y_axis < 0:
                                    command = "diagonal_front_right"
                                elif x_axis < 0 and y_axis > 0:
                                    command = "diagonal_back_left"
                                elif x_axis < 0 and y_axis < 0:
                                    command = "diagonal_front_left"
                            elif abs(x_axis)> action_threshold:
                                if x_axis > 0:
                                    command = "lateral_right"
                                else:
                                    command = "lateral_left"
                            elif abs(y_axis) > action_threshold:
                                if y_axis > 0:
                                    command = "backward"
                                else:
                                    command = "forward"
                            elif abs(x_axis_rot) > action_threshold:
                                if x_axis_rot > 0:
                                    command = "spin_R"
                                else:
                                    command = "spin_L"  
                            elif boton_stop == True:
                                print("Boton stop")
                                command = "stop"
                            last_action_time = current_time
                            action_triggered = False

                            # Send the command to the server
                            self.client_socket.sendall(command.encode())
                            print("Enviando comando:", command)

                            if boton_exit == True:
                                command = 'stop'
                                # Send the command to the server
                                self.client_socket.sendall(command.encode())
                                print("Enviando comando de cierre:", command)
                                exit()


        finally:
            # Close the client socket
            self.client_socket.close()

def run_video_receiver(server_url):
    video_receiver = VideoReceiver(server_url)
    video_receiver.start_receiving()

def run_remote_control(server_address, server_port):
    remote_control = RemoteControl(server_address, server_port)
    remote_control.connect()

def main():
    server_url =  'ws://192.168.0.103:8765'  # Replace with the WebSocket server URL
    #server_url = 'ws://omni.local:8765'
    server_address = '192.168.0.103'
    #server_url =  'ws://192.168.80.156:8765'  # Replace with the WebSocket server URL
    # server_address = '192.168.246.199'  # Replace with the IP/hostname address of your Raspberry Pi
    server_port = 5000

    video_thread = threading.Thread(target=run_video_receiver, args=(server_url,))
    remote_control_thread = threading.Thread(target=run_remote_control, args=(server_address, server_port))


    video_thread.start()
    remote_control_thread.start()


    video_thread.join()
    remote_control_thread.join()


if __name__ == "__main__":
    main()




 