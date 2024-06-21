import socket

ip = '0.0.0.0'
port = 23456
# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))  # Bind to all available interfaces and a specific port
server_socket.listen()

print('Server is listening...')

while True:
    # Accept a client connection
    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')

    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                break  # Break the loop if no data is received

            print(f'Received from client: {data.decode()}')

            # Echo back the received data
            conn.sendall(data)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        conn.close()
        print(f'Connection closed by {addr}')

# Close the server socket
server_socket.close()
