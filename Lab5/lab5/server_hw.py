import os
import json
import base64
import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

SERVER_MEDIA = "SERVER_MEDIA"
if not os.path.exists(SERVER_MEDIA):
    os.makedirs(SERVER_MEDIA)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = {}


def recv_all(sock, size):
    chunks = []
    bytes_received = 0
    while bytes_received < size:
        chunk = sock.recv(min(size - bytes_received, 2048))
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_received += len(chunk)
    return b''.join(chunks)


def handle_client(client_socket, client_address):
    username = None
    room = None

    try:
        while True:
            header_data = client_socket.recv(1024).decode('utf-8')
            if not header_data:
                break

            header = json.loads(header_data)
            msg_length = header['length']
            data = recv_all(client_socket, msg_length)
            received_message = json.loads(data.decode('utf-8'))
            message_type = received_message["type"]

            if message_type == "handshake":
                username = received_message["payload"]["username"]
                room = received_message["payload"]["room"]
                clients[client_socket] = {"username": username, "room": room}
            elif message_type == "message":
                broadcast_message = {
                    "type": "message",
                    "payload": {"sender": username, "content": received_message["payload"]["content"]}
                }
                broadcast(json.dumps(broadcast_message), room)
            elif message_type == "upload":
                # ensure roomspecific dir exists
                room_folder = os.path.join(SERVER_MEDIA, room)
                if not os.path.exists(room_folder):
                    os.makedirs(room_folder)

                # save  file inside roomspecific dir
                file_name = received_message["payload"]["file_name"]
                file_data = received_message["payload"]["file_data"]
                with open(os.path.join(room_folder, file_name), "wb") as file:
                    file.write(base64.b64decode(file_data))
                notification = {
                    "type": "notification",
                    "payload": {"message": f"User {username} uploaded the {file_name} file."}
                }
                broadcast(json.dumps(notification), room)
            elif message_type == "download":
                room_folder = os.path.join(SERVER_MEDIA, room)
                file_name = received_message["payload"]["file_name"]
                file_path = os.path.join(room_folder, file_name)
                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        file_data = base64.b64encode(
                            file.read()).decode('utf-8')
                    download_data = {
                        "type": "downloaded_file",
                        "payload": {
                            "file_name": file_name,
                            "file_data": file_data,
                        }
                    }
                    send_large_message(
                        client_socket, json.dumps(download_data))
                else:
                    notification = {
                        "type": "notification",
                        "payload": {"message": f"The {file_name} doesn't exist"}
                    }
                    send_large_message(client_socket, json.dumps(notification))

    except Exception as e:
        print(f"An error occurred with client {client_address}: {e}")
    finally:
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]


def send_large_message(client, message):
    header = {
        'length': len(message.encode('utf-8'))
    }
    client.send(json.dumps(header).encode('utf-8'))
    client.send(message.encode('utf-8'))


def broadcast(message, room):
    for client, client_data in clients.items():
        if client_data["room"] == room:
            send_large_message(client, message)


def main():
    print("Server started and listening...")
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(
            client_socket, client_address)).start()


if __name__ == "__main__":
    main()
