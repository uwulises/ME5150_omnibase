import socket

class PCClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.socket.connect((self.server_ip, self.server_port))
    
    def send_text(self, text_message):
        self.socket.sendall(text_message.encode('utf-8'))
        print("Text message sent:", text_message)
    
    def receive_image(self, image_save_path):
        with open(image_save_path, 'wb') as f:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                f.write(data)
        print("Image received and saved as", image_save_path)
    
    def close(self):
        self.socket.close()

def main():
    # Example usage
    server_ip = '192.168.1.23'  # Replace with the IP address of your RPI
    server_port = 12345
    text_message = 'Hello Raspberry Pi'
    image_save_path = 'received_image.jpg'

    client = PCClient(server_ip, server_port)
    client.connect()
    while True:
        client.send_text(text_message)
    # client.receive_image(image_save_path)
    client.close()

if __name__ == '__main__':
    main()