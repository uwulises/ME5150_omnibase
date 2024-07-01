import socket
import time

class ControlClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")
        time.sleep(2)

    def _send_message(self, msg):
        try:
            self.socket.sendall(msg.encode())
            print(f"Sent to server: {msg}")

        except Exception as e:
            print(f"Error sending data: {e}")
            raise TimeoutError

    def _receive_message(self):
        try:
            data = self.socket.recv(1024)
            print(f"Received from server: {data.decode()}")
            return data.decode()

        except Exception as e:
            print(f"Error receiving data: {e}")

    def _disconnect(self):
        self.socket.close()
        print("Disconnected from server")

    def check_connection_and_fix(self): 
        connected = False  
        print("Connection lost, reconnecting...")  
        while not connected:  
            try:
                self._disconnect()  
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(3)
                self.socket.connect((self.server_ip, self.server_port))  
                connected = True  
                print("Re-connection successful") 
                time.sleep(1) 
            except socket.error as e:
                # print(e)
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
                print(f"Received from server: {data.decode()}")
                if 'OK' in data.decode():
                    print("Received OK from server")
                    ready = True

            except KeyboardInterrupt:
                self._disconnect()
                break
            # Si es un error de timeout, se intenta reconectar
            except socket.timeout as e:
                print(f"Error receiving data: {e}, retrying...")

            except Exception as e:
                # print(f"Error sending data: {e}")
                self.check_connection_and_fix()
            retries += 1
        time.sleep(1)
        
def main():
    ip_server = 'omni1.local'
    ip_server = '192.168.166.233'
    client = ControlClient(ip_server, 12345)
    msg = 'x:0.5,y:0.0,o:0,dt:0.1,t_max:2' # x[mm], y[mm], o[rad], dt[s], t_max[s
    client.send(msg)
    msg = 'x:0.0,y:0.2,o:0,dt:0.1,t_max:2'
    client.send(msg)
    client._disconnect()
if __name__ == '__main__':
    main()