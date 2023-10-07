import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345  # Server's port

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

# Function to receive and display messages
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break  # Exit the loop when the server disconnects
        print(f"Received: {message}")


# Start the message reception thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True  # Thread will exit when the main program exits
receive_thread.start()

while True:
    message = input("Enter a message (or 'exit' to quit): ")

    if message.lower() == 'exit':
        break  # Exit the main loop when 'exit' is entered

    # Send the message to the server
    client_socket.send(message.encode('utf-8'))

# Close the client socket when done
client_socket.close()
