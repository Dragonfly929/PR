import socket
import threading
import json
import os

HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


name = input("Enter your name: ")
room = input("Enter the room name: ")

def receive_messages():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = json.loads(data.decode('utf-8'))
        message_type = received_message["type"]

        if message_type == "connect_ack":
            print(received_message["payload"]["message"])
        elif message_type == "message":
            sender = received_message["payload"]["sender"]
            received_room = received_message["payload"]["room"]
            message_text = received_message["payload"]["text"]
            print(f"[{received_room}] {sender}: {message_text}")
        elif message_type == "notification":
            notification_message = received_message["payload"]["message"]
            print(f"Notification: {notification_message}")

def send_message():
    global room
    while True:
        message = input("Enter a message or file command (e.g., 'upload: path/to/file.txt', 'download: file.txt', or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        elif message.startswith("upload: "):
            file_path = message.split("upload: ")[1]
            send_upload_command(file_path)
        elif message.startswith("download: "):
            file_name = message.split("download: ")[1]
            send_download_command(file_name)
        else:
            message_data = {
                "type": "message",
                "payload": {
                    "sender": name,
                    "room": room,
                    "text": message,
                },
            }
            client_socket.send(json.dumps(message_data).encode('utf-8'))

def send_upload_command(file_path):
    if os.path.exists(file_path):
        upload_data = {
            "type": "upload",
            "payload": {
                "path": file_path
            }
        }
        client_socket.send(json.dumps(upload_data).encode('utf-8'))
    else:
        print(f"File '{file_path}' doesn't exist.")

def send_download_command(file_name):
    download_data = {
        "type": "download",
        "payload": {
            "filename": file_name
        }
    }
    client_socket.send(json.dumps(download_data).encode('utf-8'))
    file_data = client_socket.recv(1024)

    if file_data.startswith(b'{"type":"notification"'):
        notification = json.loads(file_data.decode('utf-8'))
        print(notification["payload"]["message"])
    else:
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print(f"Downloaded {file_name}")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.daemon = True
send_thread.start()

send_thread.join()