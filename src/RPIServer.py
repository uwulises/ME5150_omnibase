import socket

import socket

class RPIServer:
    def __init__(self, server_ip, server_port, image_path):
        self.server_ip = server_ip
        self.server_port = server_port
        self.image_path = image_path
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse address option
    
    def start(self):
        self.socket.bind((self.server_ip, self.server_port))
        self.socket.listen(1)
        print("Server listening on {}:{}".format(self.server_ip, self.server_port))
        while True:
            client_socket, addr = self.socket.accept()
            print("Connected by", addr)
            try:
                self.handle_client(client_socket)
            finally:
                client_socket.close()
    
    def handle_client(self, client_socket):
        text_message = self.receive_text(client_socket)
        print("Received text message:", text_message)
        self.send_image(client_socket)
        print("Image sent to client")
    
    def receive_text(self, client_socket):
        return client_socket.recv(1024).decode('utf-8')
    
    def send_image(self, client_socket):
        with open(self.image_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
    
    def close(self):
        self.socket.close()

def main():
    # Example usage
    server_ip = '0.0.0.0'  # Bind to all interfaces
    server_port = 22
    image_path = 'path_to_image.jpg'  # Replace with the path to your image

    server = RPIServer(server_ip, server_port, image_path)
    server.start()
    while True:
        server.receive_text()


if __name__ == '__main__':
    main()