import socket
import time
from picamera2 import Picamera2
import io

class RPIServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn = None
        self.client_addr = None
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # Acepta una sola conexión

        print(f'Server is listening on {self.host}:{self.port}...')

        self.picam2 = Picamera2()
        self.picam2.configure("still")
        self.picam2.start()

        # Give time for AEC and AWB to settle
        time.sleep(1)
        self.picam2.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
        print("Camera configured")
        time.sleep(1)

    def accept_connection(self):
        try:
            conn, addr = self.server_socket.accept()
            print(f'Connected by {addr}')
            self.client_conn = conn
            self.client_addr = addr
            return True
        except socket.timeout:
            print("Timeout while waiting for a connection.")
            return False
        except Exception as e:
            print(f"Error accepting connection: {e}")
            return False

    def receive_message(self):
        if not self.client_conn:
            print("No client connected.")
            return None

        try:
            data = self.client_conn.recv(1024)
            return data.decode()

        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def close_connection(self):
        if self.client_conn:
            self.client_conn.close()
            print(f'Connection closed by {self.client_addr}')
            self.client_conn = None

    def send_confirmation(self):
        print('Sending confirmation to client...')
        try:
            msg = 'OK'
            self.client_conn.sendall(msg.encode())
            print('Confirmation sent to client')
        except Exception as e:
            print(f"Error sending confirmation: {e}")

    def send_enm(self):
        print('Sending enm to client...')
        try: #as bytes
            msg = b'EOM'
            self.client_conn.sendall(msg)
            print('ENM sent to client')
        except Exception as e:
            print(f"Error sending enm: {e}")

    def send_image(self):
        print('Sending image to client...')
        try:
            # Capture a single frame
            stream = io.BytesIO()
            print("Capturing image...")
            image = self.picam2.capture_image()
            image.save(stream, format='jpeg')
            print("Image captured")
            
            # Send the image
            stream.seek(0)
            total_size = stream.getbuffer().nbytes
            while True:
                # print("Sending image data...")
                data = stream.read(1024)
                
                if stream.tell() >= total_size:  # Check if the end of the stream is reached
                    self.send_enm()
                    break
                self.client_conn.sendall(data)

        except Exception as e:
            print(f"Error sending image: {e}")
            raise


def main():
    server = RPIServer('0.0.0.0', 12345)
    dt_image = time.time()

    while True:
        if server.client_conn is None:
            print("No client connected. Attempting to accept a new connection...")
            server.accept_connection()
        else:
            if time.time() - dt_image > 0.5:
                server.send_image()
                dt_image = time.time
            
            message = server.receive_message()
            if message:
                print("Received:", message)
                server.send_confirmation()

        time.sleep(0.1)

    server.close_connection()



if __name__ == '__main__':
    main()