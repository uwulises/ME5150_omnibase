import socket
import time
# from picamera2 import Picamera2
import io

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn = None
        self.client_addr = None

        # self.picam2 = Picamera2()
        # self.picam2.configure("still")
        # self.picam2.start()

        # # Give time for AEC and AWB to settle
        # time.sleep(1)
        # self.picam2.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": 1.0})
        # time.sleep(1)


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # Acepta una sola conexión
        print(f'Server is listening on {self.host}:{self.port}...')

        try:
            conn, addr = self.server_socket.accept()
            print(f'Connected by {addr}')
            self.client_conn = conn
            self.client_addr = addr
            return True
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.server_socket.close()
            return False

    def receive_message(self):
        if not self.client_conn:
            print("No client connected.")
            return None
        
        try:
            data = self.client_conn.recv(1024)
            if not data:
                print(f'Connection closed by {self.client_addr}')
                self.client_conn.close()
                self.client_conn = None
                return None
            else:
                print(f'Received from client at {self.client_addr}: {data.decode()}')
                return data.decode()
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def close_connection(self):
        if self.client_conn:
            self.client_conn.close()
            print(f'Connection closed by {self.client_addr}')
            self.client_conn = None

if __name__ == '__main__':
    server = TCPServer('0.0.0.0', 23456)
    
    if server.start():
        while True:
            message = server.receive_message()

            if message:
                print("Received:", message)
                # Aquí puedes agregar lógica adicional según lo que desees hacer con el mensaje recibido
            else:
                print('naita')
    
    server.close_connection()
