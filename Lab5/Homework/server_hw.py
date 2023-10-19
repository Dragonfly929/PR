import socket
import threading
import json
import os
import base64

HOST = '127.0.0.1'
PORT = 8083

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

connected_clients = {}

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

def broadcast_notification(room, message):
    for client_socket, client_info in connected_clients.items():
        if client_info["room"] == room:
            notification_data = {
                "type": "notification",
                "payload": {"message": message},
            }
            client_socket.send(json.dumps(notification_data).encode('utf-8'))

def handle_file_upload(client_socket, image_name, image_data):
    try:
        room_folder = os.path.join("SERVER_MEDIA", connected_clients[client_socket]["room"])
        if not os.path.exists(room_folder):
            os.makedirs(room_folder)

        image_path = os.path.join(room_folder, image_name)

        with open(image_path, "wb") as image_file:
            image_file.write(base64.b64decode(image_data.encode('utf-8')))

        notification_message = f"User {connected_clients[client_socket]['name']} uploaded {image_name}"
        broadcast_notification(connected_clients[client_socket]["room"], notification_message)

    except Exception as e:
        print(f"Error handling image upload: {e}")

def handle_file_download(client_socket, image_name):
    try:
        room_folder = os.path.join("SERVER_MEDIA", connected_clients[client_socket]["room"])
        image_path = os.path.join(room_folder, image_name)

        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            download_data = {
                "type": "downloaded_image",
                "payload": {
                    "image_name": image_name,
                    "image_data": image_data,
                }
            }

            client_socket.send(json.dumps(download_data).encode('utf-8'))
        else:
            not_found_data = {
                "type": "notification",
                "payload": {"message": f"The {image_name} doesn't exist."}
            }
            client_socket.send(json.dumps(not_found_data).encode('utf-8'))

    except Exception as e:
        print(f"Error handling file download: {e}")

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
            message_type = received_message["type"]
            if message_type == "message":
                message_text = received_message["payload"]["text"]
                broadcast_message(client_socket, room, message_text)
            elif message_type == "upload":
                image_name = received_message["payload"]["image_name"]
                image_data = received_message["payload"]["image_data"]
                handle_file_upload(client_socket, image_name, image_data)
            elif message_type == "download":
                image_name = received_message["payload"]["image_name"]
                handle_file_download(client_socket, image_name)

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