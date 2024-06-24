import socket
import time

class PCClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def _send_message(self, msg):
        try:
            if msg.lower() == 'exit':
                self.close()
                return
            
            self.socket.sendall(msg.encode())
            print(f"Sent to server: {msg}")
            time.sleep(1)  # Espera 1 segundo antes de enviar el próximo mensaje

        except Exception as e:
            if e.errno == 10057:
                print(f"Not connected to server")
            else:
                print(f"Error sending data: {e}")
            self._connect()

    def _receive_message(self):
        try:
            data = self.socket.recv(1024)
            if not data:
                print("Connection closed by server.")
                self._connect()
            else:
                print(f"Received from server: {data.decode()}")
                return data.decode()

        except Exception as e:
            print(f"Error receiving data: {e}")
            self._connect()

    def _connect(self):
        print("Attempting to connect...")
        while True:
            try:
                self.socket.connect((self.server_ip, self.server_port))
                print(f"Connected to server at {self.server_ip}:{self.server_port}")
                return
            except Exception as e:
                if e.errno == 10061:
                    print(f"Connection attempt failed: Server may be down, retrying in 5 seconds...")
                    time.sleep(5)
                elif e.errno == 10056:
                    print(f"Connection attempt failed: {e}, retrying in 5 seconds...")
                    time.sleep(2)  # Espera 1 segundo antes de intentar nuevamente
                else:
                    print(f"Connection attempt failed: {e}")
                    time.sleep(1)

    def _close(self):
        try:
            self.socket.close()
            print("Connection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")

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

    def send(self, msg):
        ready = False
        while not ready:
            # Intenta conectarse al servidor, si no esta conectado ya
            if not self.socket:
                self._connect()
            else:
                try:
                    self._send_message(msg)
                    print('msg send')
                    msg = self._receive_message()
                    if 'OK' in msg:
                        ready = True
                except KeyboardInterrupt:
                    self._close()
                    break
        
def main():
    ip_server = 'omni1.local'
    ip_server = '192.168.166.233'
    client = PCClient(ip_server, 12345)
    
    client.send('lalalla')

if __name__ == '__main__':
    main()