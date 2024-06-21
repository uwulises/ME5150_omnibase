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
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise
    
    def send_message(self, msg):
        try:
            if msg.lower() == 'exit':
                self.close()
                return
            
            self.socket.sendall(msg.encode())
            print(f"Sent to server: {msg}")
            time.sleep(1)  # Wait for 1 second before sending the next message

        except Exception as e:
            print(f"Error sending data: {e}")
            raise
    
    def close(self):
        try:
            self.socket.close()
            print("Connection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")
            raise

# Usage
if __name__ == '__main__':
    client = PCClient('omni1.local', 23456)
    client.connect()
    try:

        while True:
            
            client.send_message('alo')
    finally:
        client.close()