import socket

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f'Server is listening on {self.host}:{self.port}...')

    def start(self):
        try:
            # while True:
            conn, addr = self.server_socket.accept()
            print(f'Connected by {addr}')
                
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()

    def listen(self):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f'Received from client at {addr}: {data.decode()}')
                return data.decode()
        except Exception as e:
            print(f"Error: {e}")

        finally:
            conn.close()
            print(f'Connection closed by {addr}')
if __name__ == '__main__':
    server = TCPServer('0.0.0.0', 23456)
    server.start()

    for i in range(100):
        data = server.listen()
        time.sleep(1)
        if data == 'exit':
            break
    
    server.close()
