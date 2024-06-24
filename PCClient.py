import socket
import time

class PCClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        self.socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")


    def _send_message(self, msg):
        try:
            self.socket.sendall(msg.encode())
            print(f"Sent to server: {msg}")

        except Exception as e:
            print(f"Error sending data: {e}")
            raise TimeoutError
            # self._close()

    def _receive_message(self):
        try:
            data = self.socket.recv(1024)
            print(f"Received from server: {data.decode()}")
            return data.decode()

        except Exception as e:
            print(f"Error receiving data: {e}")
            # self._close()
            

    # def _connect(self):
    #     print("Attempting to connect...")
    #     while True:
    #         try:
    #             self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             self.socket.connect((self.server_ip, self.server_port))
    #             print(f"Connected to server at {self.server_ip}:{self.server_port}")
    #             time.sleep(2) 
    #         except Exception as e:
    #             if e.errno == 10061:
    #                 print(f"Connection attempt failed: Server may be down, retrying in 5 seconds...")
    #                 time.sleep(5)
    #             elif e.errno == 10056:
    #                 print(f"Connection attempt failed: {e}, retrying in 5 seconds...")
    #                 time.sleep(2)
    #             else:
    #                 print(f"Connection attempt failed: {e}")
    #                 time.sleep(1)

    # def _close(self):
    #     if self.socket:
    #         self.socket.close()
    #         self.socket = None
    #         print("Connection closed")

    def receive_image(self, image_save_path):
        print("Receiving image...")
        try:
            with open(image_save_path, 'wb') as f:
                while True:
                    data = self.socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print("Image received and saved as", image_save_path)
        except Exception as e:
            print(f"Error receiving image: {e}")
            

    def check_connection_and_fix(self): 
        connected = False  
        print("Connection lost, reconnecting...")  
        while not connected:  
            try:  
                self.socket.connect((self.server_ip, self.server_port))  
                connected = True  
                print("Re-connection successful")  
            except socket.error as e:
                print(e)
                print("Re-connection failed... retrying")
                time.sleep(2)

    def send(self, msg):
        ready = False
        retries = 0
        while not ready and retries < 3:
            try:
                self._send_message(msg)
                time.sleep(0.2)
                print("Sent message, waiting for response...")
                data = self.socket.recv(1024)
                if msg is not None:
                    ready = True

            except KeyboardInterrupt:
                self._close()
                break
            # Si es un erro de timeout, se intenta reconectar
            except socket.timeout as e:
                print(f"Error receiving data: {e}, retrying...")

            except Exception as e:
                print(f"Error sending data: {e}")
                self.check_connection_and_fix()

            retries += 1
        
def main():
    ip_server = 'omni1.local'
    ip_server = '192.168.166.233'
    client = PCClient(ip_server, 12345)
    
    client.send('lalalla')
    client.receive_image('image.jpg')

if __name__ == '__main__':
    main()