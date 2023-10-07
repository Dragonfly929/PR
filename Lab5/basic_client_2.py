import socket

from Lab5.basic_server_1 import server_socket

# Server configuration
HOST = '127.0.0.1' # Server's IP address
PORT = 12345 # Server's port

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")
while True:
    message = input("Enter a message (or 'exit' to quit): ")

    if message.lower() == 'exit':
        break
    # Send the message to the server
    client_socket.send(message.encode('utf-8'))
    # Receive and display the server's response
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received: {response}")
# Close the client socket
client_socket.close()
