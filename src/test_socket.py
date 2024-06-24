import socket
import time

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn = None
        self.client_addr = None

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # Acepta una sola conexión
        print(f'Server is listening on {self.host}:{self.port}...')

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
            if not data:
                print(f'Connection closed by {self.client_addr}')
                self.client_conn.close()
                self.client_conn = None
                return None
            else:
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
       
        try:
            self.client_conn.sendall(b'OK')
            print('Confirmation sent to client')
        except Exception as e:
            print(f"Error sending confirmation: {e}")

if __name__ == '__main__':
    server = TCPServer('0.0.0.0', 12345)
    server.start()

    while True:
        if server.client_conn is None:
            print("No client connected. Attempting to accept a new connection...")
            server.accept_connection()
        else:
            message = server.receive_message()
            if message:
                print("Received:", message)
                server.send_confirmation()
                # Aquí puedes agregar lógica adicional según lo que desees hacer con el mensaje recibido
            else:
                print('No message received or connection closed.')

        time.sleep(1)

    server.close_connection()
