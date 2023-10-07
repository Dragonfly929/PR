import socket
import threading
import json


HOST = '127.0.0.1' # Server's IP address
PORT = 12345 # Server's port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = json.loads(data.decode('utf-8'))
        if received_message["type"] == "connect_ack":
            print(received_message["payload"]["message"])
        elif received_message["type"] == "message":
            sender = received_message["payload"]["sender"]
            room = received_message["payload"]["room"]
            message_text = received_message["payload"]["text"]
            print(f"[{room}] {sender}: {message_text}")
        elif received_message["type"] == "notification":
            notification_message = received_message["payload"]["message"]
            print(f"Notification: {notification_message}")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

def send_message():
    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        message_data = {
            "type": "message",
            "payload": {
                "sender": name,
                "room": room,
                "text": message,
            },
        }
        client_socket.send(json.dumps(message_data).encode('utf-8'))

# Prompt the user for their name and room
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


send_thread.join()
