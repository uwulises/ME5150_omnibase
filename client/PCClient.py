import socket
import time

class ControlClient:
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
                if 'OK' in data.decode():
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
    client = ControlClient(ip_server, 12345)
    msg = 'x:0.1,y:0.1,o:0,dt:1,t_max:5' # x[mm], y[mm], o[rad], dt[s], t_max[s
    client.send(msg)
    print("Message sent")
    time.sleep(5)
    # print("Receiving image...")
    # msg = 'x:0.2,y:0.0,o:0,dt:0.1,t_max:5'
    # client.send(msg)
    print("Message sent")
if __name__ == '__main__':
    main()