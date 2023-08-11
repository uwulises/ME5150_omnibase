import threading
import asyncio
import websockets
import base64
import cv2
import numpy as np
import socket
import keyboard

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

            while True:
                # Wait for a key press event
                key_event = keyboard.read_event()

                if key_event.event_type == 'down':
                    # Map key press events to commands
                    if key_event.name == 'w':
                        command = 'forward'
                    elif key_event.name == 's':
                        command = 'backward'
                    elif key_event.name == 'q':
                        command = 'spin_L'
                    elif key_event.name == 'e':
                        command = 'spin_R'
                    elif key_event.name == 'a':
                        command = 'lateral_left'
                    elif key_event.name == 'd':
                        command = 'lateral_right'
                    else:
                        command = 'stop'

                    # Send the command to the server
                    self.client_socket.sendall(command.encode())

                    if key_event.name == 'esc':
                        command = 'stop'
                        # Send the command to the server
                        self.client_socket.sendall(command.encode())
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
    server_url = 'ws://omni2.local:8765'  # Replace with the WebSocket server URL
    server_address = 'omni2.local'  # Replace with the IP/hostname address of your Raspberry Pi
    server_port = 5000

    video_thread = threading.Thread(target=run_video_receiver, args=(server_url,))
    remote_control_thread = threading.Thread(target=run_remote_control, args=(server_address, server_port))

    video_thread.start()
    remote_control_thread.start()

    video_thread.join()
    remote_control_thread.join()

if __name__ == "__main__":
    main()
