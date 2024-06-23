import socket
import time

class PCClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        
    
    def send_message(self, msg):
      while True:
        try:            
            self.socket.sendall(msg.encode())
            print(f"Sent to server: {msg}")
            time.sleep(1)  # Espera 1 segundo antes de enviar el próximo mensaje
            break

        except Exception as e:
            print(f"Error sending data: {e}")
            self.connect()

    def receive_message(self):
        try:
            data = self.socket.recv(1024)
            if not data:
                print("Connection closed by server.")
                self.connect()
            else:
                print(f"Received from server: {data.decode()}")

        except Exception as e:
            print(f"Error receiving data: {e}")
            self.connect()

    def connect(self):
        print("Attempting to connect...")
        while True:
            try: 
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server_ip, self.server_port))
                print(f"Connected to server at {self.server_ip}:{self.server_port}")
                break
            except Exception as e:
                print(f"Connection attempt failed: {e}")
                time.sleep(1)  # Espera 1 segundo antes de intentar nuevamente

    def close(self):
        try:
            self.socket.close()
            print("Connection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")

# Uso del cliente
if __name__ == '__main__':
    client = PCClient('omni1.local', 23456)
    while True:
        try:
            msg = input("Enter a message: ")
            client.send_message(msg)
        except KeyboardInterrupt:
            client.close()
            break

