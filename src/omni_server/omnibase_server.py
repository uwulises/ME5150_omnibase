import asyncio
import websockets
import base64
import picamera
import io
import time
import socket
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
from threading import Thread

class VideoServer:
    def __init__(self):
        self.camera = None
        self.frame_count = 0
        self.max_frame_count = 2

    async def send_video(self, websocket, path):
        # Set up the Raspberry Pi camera
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.iso = 800
        self.camera.awb_mode = 'sunlight'
        self.camera.shutter_speed = 30000
        time.sleep(1)

        try:
            # Continuously capture and send video frames
            while True:
                # Capture a frame
                stream = io.BytesIO()
                self.camera.capture(stream, format='jpeg', use_video_port=True)

                # Skip frames according to the frame count
                self.frame_count += 1
                if self.frame_count % self.max_frame_count != 0:
                    # Delete the captured frame without sending it
                    stream.close()
                    continue

                # Read the captured frame
                stream.seek(0)
                encoded_image = base64.b64encode(stream.read()).decode('utf-8')

                try:
                    # Send the frame to the client
                    await websocket.send(encoded_image)
                except websockets.exceptions.ConnectionClosed:
                    # Connection closed by the client
                    print("Client connection closed")
                    break

                # Delete the captured frame
                stream.close()

        finally:
            # Clean up resources
            self.camera.close()

    async def start_server(self):
        server = await websockets.serve(self.send_video, '0.0.0.0', 8765)

        # Keep the server running until interrupted
        await server.wait_closed()

class DriveServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.base_comm = None

    def start(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set up the server address and port
        server_address = (self.host, self.port)
        self.server_socket.bind(server_address)

        self.base_comm = SerialControl()
        self.base_comm.open_serial()

        # Listen for incoming connections
        self.server_socket.listen(1)

        print('Server is up and listening for connections...')

        try:
            while True:
                # Wait for a client to connect
                print('Waiting for a client to connect...')
                client_socket, client_address = self.server_socket.accept()
                print(f'Client connected: {client_address}')

                while True:
                    # Receive data from the client
                    data = client_socket.recv(1024).decode().strip()
                    if not data:
                        # No more data from the client
                        break

                    # Process the received data and control the motors
                    if data == 'forward':
                        self.base_comm.forward()
                    elif data == 'backward':
                        self.base_comm.backward()
                    elif data == 'spin_L':
                        self.base_comm.spin_left()
                    elif data == 'spin_R':
                        self.base_comm.spin_right()
                    elif data == 'lateral_left':
                        self.base_comm.lateral_left()
                    elif data == 'lateral_right':
                        self.base_comm.lateral_right()
                    elif data == 'diagonal_front_left':
                        self.base_comm.diagonal_front_left()
                    elif data == 'diagonal_front_right':
                        self.base_comm.diagonal_front_right()
                    elif data == 'diagonal_back_left':
                        self.base_comm.diagonal_back_left()
                    elif data == 'diagonal_back_right':
                        self.base_comm.diagonal_back_right()
                    elif data == 'stop':
                        self.base_comm.stop()
                    else:
                        print(f'Invalid command: {data}')

                print(f'Client disconnected: {client_address}')

        finally:
            # Close the server socket
            self.server_socket.close()

if __name__ == "__main__":
    video_server = VideoServer()
    drive_server = DriveServer('omni.local', 5000)

    # Start video server in a separate thread
    video_thread = Thread(target=asyncio.run, args=(video_server.start_server(),))
    video_thread.start()

    # Start drive server in the main thread
    drive_server.start()
