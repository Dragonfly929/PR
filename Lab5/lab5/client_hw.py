import os
import uuid
import base64
import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

CLIENT_MEDIA = os.path.join("CLIENT_MEDIA", str(uuid.uuid4()))
if not os.path.exists(CLIENT_MEDIA):
    os.makedirs(CLIENT_MEDIA)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


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


def handle_downloaded_file(received_message):
    file_name = received_message["payload"]["file_name"]
    file_data = received_message["payload"]["file_data"]
    with open(os.path.join(CLIENT_MEDIA, file_name), "wb") as file:
        file.write(base64.b64decode(file_data))
    print(f"File {file_name} downloaded successfully.")


def receive_messages():
    while True:
        try:
            header_data = client_socket.recv(1024).decode('utf-8')
            if not header_data:
                print("Disconnected from server.")
                break

            header = json.loads(header_data)
            msg_length = header['length']
            data = recv_all(client_socket, msg_length)

            received_message = json.loads(data.decode('utf-8'))
            message_type = received_message["type"]

            if message_type == "message":
                print(
                    f"{received_message['payload']['sender']}: {received_message['payload']['content']}")
            elif message_type == "notification":
                print(received_message["payload"]["message"])
            elif message_type == "downloaded_file":
                handle_downloaded_file(received_message)
            else:
                print("Unknown message type:", message_type)

        except Exception as e:
            print(f"An error occurred: {e}")
            break


threading.Thread(target=receive_messages, daemon=True).start()


def send_large_message(message):
    header = {
        'length': len(message.encode('utf-8'))
    }
    client_socket.send(json.dumps(header).encode('utf-8'))
    client_socket.send(message.encode('utf-8'))


def send_message():
    username = input("Enter your name: ")
    room = input("Enter room name: ")

    handshake_data = {
        "type": "handshake",
        "payload": {"username": username, "room": room}
    }
    send_large_message(json.dumps(handshake_data))

    while True:
        message = input(
            "Enter a message (or 'upload: <path to file>', 'download: <file name>', or 'exit' to quit): ")

        if message == "exit":
            break
        elif message.startswith("upload: "):
            file_path = message[8:]
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    file_data = base64.b64encode(file.read()).decode('utf-8')
                upload_data = {
                    "type": "upload",
                    "payload": {
                        "file_name": os.path.basename(file_path),
                        "file_data": file_data,
                    }
                }
                send_large_message(json.dumps(upload_data))
            else:
                print(f"File {file_path} doesn't exist.")
        elif message.startswith("download: "):
            download_command = {
                "type": "download",
                "payload": {"file_name": message[10:], }
            }
            send_large_message(json.dumps(download_command))
        else:
            send_large_message(json.dumps({
                "type": "message",
                "payload": {"content": message}
            }))


send_message()
client_socket.close()
