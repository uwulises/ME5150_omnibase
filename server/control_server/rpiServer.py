import socket
import time
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
    
    def is_client_connected(self):
        if self.client_conn:
            try:
                data = self.client_conn.recv(1024)
                if data == b'':
                    print("Client disconnected")
                    return False
                return True
            except BlockingIOError:
                # No data available, client is still connected
                return True
            except ConnectionResetError:
                print("Connection reset by peer")
                return False
            except Exception as e:
                print(f"Error checking client connection: {e}")
                return False
        return False

def main():
    server = RPIServer('0.0.0.0', 12345)
    while True:
        if not server.is_client_connected():
            print("No client connected. Attempting to accept a new connection...")
            server.accept_connection()
        else:     
            print("Receiving message...")       
            message = server.receive_message()
            if message:
                print("Received:", message)
                # time.sleep(5)
                server.send_confirmation()
    server.close_connection()

if __name__ == '__main__':
    main()