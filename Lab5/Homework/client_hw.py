import socket
import threading
import json
import os
import base64

HOST = '127.0.0.1'
PORT = 8083

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

if not os.path.exists("CLIENT_MEDIA"):
    os.makedirs("CLIENT_MEDIA")

def handle_downloaded_image(received_message):
    image_name = received_message["payload"]["image_name"]

    if image_name.startswith("The "):
        print(image_name)
    else:
        image_data = received_message["payload"]["image_data"]
        with open(f"CLIENT_MEDIA/{image_name}", "wb") as image_file:
            image_file.write(base64.b64decode(image_data))
        print(f"File {image_name} downloaded successfully.")

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
            room = received_message["payload"]["room"]
            message_text = received_message["payload"]["text"]
            print(f"[{room}] {sender}: {message_text}")
        elif message_type == "notification":
            notification_message = received_message["payload"]["message"]
            print(f"Notification: {notification_message}")
        elif message_type == "downloaded_image":
            handle_downloaded_image(received_message)

def send_message():
    while True:
        message = input(
            "Enter a message (or 'upload: <path to image file>', 'download: <image name>', or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        if message.startswith("upload: "):
            image_path = message[8:]
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                upload_data = {
                    "type": "upload",
                    "payload": {
                        "image_name": os.path.basename(image_path),
                        "image_data": image_data,
                    }
                }
                client_socket.send(json.dumps(upload_data).encode('utf-8'))
            else:
                print(f"File {image_path} doesn't exist.")
        elif message.startswith("download: "):
            download_command = {
                "type": "download",
                "payload": {
                    "image_name": message[10:],
                }
            }
            client_socket.send(json.dumps(download_command).encode('utf-8'))
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


name = input("Enter your name: ")
room = input("Enter the room name: ")

connect_data = {
    "type": "connect",
    "payload": {
        "name": name,
        "room": room,
    },
}
client_socket.send(json.dumps(connect_data).encode('utf-8'))

send_thread = threading.Thread(target=send_message)
send_thread.daemon = True
send_thread.start()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

send_thread.join()