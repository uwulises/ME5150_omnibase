import socket
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
import time 

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up the server address and port
server_address = ('omni.local', 5000)  # Use any available IP address
server_socket.bind(server_address)

base_comm = SerialControl()
base_comm.open_serial()


# Listen for incoming connections
server_socket.listen(1)

print('Server is up and listening for connections...')

try:
    
    while True:
        # Wait for a client to connect
        print('Waiting for a client to connect...')
        client_socket, client_address = server_socket.accept()
        print(f'Client connected: {client_address}')

        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode().strip()
            print(data)
            if not data:
                # No more data from the client
                break
            
            # Process the received data and control the motors
            if data == 'forward':
                base_comm.forward()
               
            elif data == 'backward':
                base_comm.backward()
            elif data == 'spin_L':
                base_comm.spin_left()
                
            elif data == 'spin_R':
                base_comm.spin_right()

            elif data == 'stop':
                base_comm.stop()
            else:
                print(f'Invalid command: {data}')

        print(f'Client disconnected: {client_address}')

finally:
    # Close the server socket
    server_socket.close()