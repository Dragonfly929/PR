import socket
import threading
import json


# Server configuration
HOST = '127.0.0.1' # Server's IP address
PORT = 12345 # Server's port


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))


connected_clients = {}  # {client_socket: {"name": name, "room": room}}


def broadcast_message(sender_socket, room, message):
    for client_socket, client_info in connected_clients.items():
        if client_info["room"] == room and client_socket != sender_socket:
            message_data = {
                "type": "message",
                "payload": {
                    "sender": connected_clients[sender_socket]["name"],
                    "room": room,
                    "text": message,
                },
            }
            client_socket.send(json.dumps(message_data).encode('utf-8'))


def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        connect_data = json.loads(data.decode('utf-8'))
        name = connect_data["payload"]["name"]
        room = connect_data["payload"]["room"]

        connected_clients[client_socket] = {"name": name, "room": room}

        notification_message = f"{name} has joined the room."
        broadcast_message(client_socket, room, notification_message)

        ack_message = {
            "type": "connect_ack",
            "payload": {"message": "Connected to the room."}
        }
        client_socket.send(json.dumps(ack_message).encode('utf-8'))

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            received_message = json.loads(data.decode('utf-8'))
            message_text = received_message["payload"]["text"]
            broadcast_message(client_socket, room, message_text)

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        if client_socket in connected_clients:
            del connected_clients[client_socket]
        client_socket.close()


server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
