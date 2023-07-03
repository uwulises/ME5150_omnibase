import socket
import keyboard

# Set up the server address and port
server_address = '192.168.73.199'  # Replace with the IP address of your Raspberry Pi
server_port = 5000

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((server_address, server_port))
    print('Connected to the server.')

    while True:
        # Wait for a key press event
        key_event = keyboard.read_event()

        if key_event.event_type == 'down':
            # Map key press events to commands
            if key_event.name == 'up':
                command = 'forward'
            elif key_event.name == 'down':
                command = 'backward'
            elif key_event.name == 'left':
                command = 'spin_L'
            elif key_event.name == 'right':
                command = 'spin_R'
            else:
                command = 'stop'

            # Send the command to the server
            client_socket.sendall(command.encode())

            if key_event.name == 'esc':
                break

finally:
    # Close the client socket
    client_socket.close()