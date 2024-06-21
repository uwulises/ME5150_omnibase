import socket
import time
# from picamera2 import Picamera2
import io

class RPIServer:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse address option
        
        self.picam2 = Picamera2()
        self.picam2.configure("still")
        self.picam2.start()

        # Give time for AEC and AWB to settle
        time.sleep(1)
        self.picam2.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
        time.sleep(1)

    def start(self):
        self.socket.bind((self.server_ip, self.server_port))
        self.socket.listen(1)
        print(f"Server listening on {self.server_ip}:{self.server_port}")
        while True:
            client_socket, addr = self.socket.accept()
            print(f"Connected by {addr}")
            try:
                self.handle_client(client_socket)
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
            finally:
                client_socket.close()

    def handle_client(self, client_socket):
        text_message = self.receive_text(client_socket)
        print("Received text message:", text_message)
        # self.send_image(client_socket)
        # print("Image sent to client")

    def receive_text(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                raise ValueError("Received empty text message")
            return data
        except Exception as e:
            print(f"Error receiving text message: {e}")
            raise

    def send_image(self, client_socket):
        try:
            # Capture a single frame
            stream = io.BytesIO()
            r = self.picam2.capture_request()
            r.save("main", stream)
            r.release()

            # Send the image
            stream.seek(0)
            while True:
                data = stream.read(1024)
                if not data:
                    break
                client_socket.sendall(data)

        except Exception as e:
            print(f"Error sending image: {e}")
            raise

    def close(self):
        self.socket.close()
        self.picam2.stop()

def main():
    server_ip = '192.168.1.23'  # Replace with the IP address of your RPI
    server_port = 12345
    
    server = RPIServer(server_ip, server_port, image_path)
    server.start()

if __name__ == '__main__':
    main()