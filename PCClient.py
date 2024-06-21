import socket
import time

class PCClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise
    
    def send_text(self, text_message):
        try:
            self.socket.sendall(text_message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending text message: {e}")
            self.close()  # Ensure socket is closed on error
            raise
    
    # def receive_image(self, image_save_path):
    #     try:
    #         with open(image_save_path, 'wb') as f:
    #             while True:
    #                 data = self.socket.recv(1024)
    #                 if not data:
    #                     break
    #                 f.write(data)
    #         print("Image received and saved as", image_save_path)
    #     except Exception as e:
    #         print(f"Error receiving image: {e}")
    #         self.close()  # Ensure socket is closed on error
    #         raise
    
    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None  


def main():
    server_ip = '192.168.1.23'  # Reemplaza con la IP de tu Raspberry Pi
    server_port = 12345
    text_message = 'Hello Raspberry Pi'
    # image_save_path = 'received_image.jpg'

    client = PCClient(server_ip, server_port)
    while True:
        try:
            client.connect()
            client.send_text(text_message)
            time.sleep(2)
            # client.receive_image(image_save_path)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client.close()
            time.sleep(2)  # Wait before attempting to reconnect

if __name__ == '__main__':
    main()