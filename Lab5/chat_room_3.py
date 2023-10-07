import socket
import threading

# ... (Code from Step 1)
# Server configuration
HOST = '127.0.0.1' # Loopback address for localhost
PORT = 12345 # Port to listen on

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    # Receive and echo back messages
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break # Exit the loop when the client disconnects
        print(f"Received: {message}")
        client_socket.send(message.encode('utf-8'))

    # Close the client socket
    client_socket.close()

# end (de from Step 1)

# Function to handle a client's messages
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break # Exit the loop when the client disconnects
        print(f"Received from {client_address}: {message}")

        # Broadcast the message to all clients
        for client in clients:
            # if client != client_socket: # find alternative to this IF
            client.send(message.encode('utf-8'))

    # Remove the client from the list
    clients.remove(client_socket)
    client_socket.close()

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

    # Start a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()