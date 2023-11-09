import os
import uuid
import base64
import json
import socket
import threading
import pika

HOST = "127.0.0.1"
PORT = 12345

CLIENT_MEDIA = os.path.join("CLIENT_MEDIA", str(uuid.uuid4()))
if not os.path.exists(CLIENT_MEDIA):
    os.makedirs(CLIENT_MEDIA)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# RabbitMQ Setup
RABBITMQ_HOST = 'localhost'
CLIENT_QUEUE = f'client_queue_{uuid.uuid4()}'
RABBITMQ_SERVER_QUEUE = 'server_queue'

credentials = pika.PlainCredentials('guest', 'guest')
connection_parameters = pika.ConnectionParameters(
    RABBITMQ_HOST, 5672, '/', credentials)
rabbitmq_connection = pika.BlockingConnection(connection_parameters)
channel = rabbitmq_connection.channel()
channel.queue_declare(queue=CLIENT_QUEUE)

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



def listen_to_rabbitmq():
    def callback(ch, method, properties, body):
        received_message = json.loads(body)
        process_received_message(received_message)

    channel.basic_consume(queue=CLIENT_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def process_received_message(received_message):
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

def send_to_rabbitmq(message):
    channel.basic_publish(exchange='', routing_key=RABBITMQ_SERVER_QUEUE, body=message)

def send_message():
    username = input("Enter your name: ")
    room = input("Enter room name: ")

    handshake_data = {
        "type": "handshake",
        "payload": {"username": username, "room": room}
    }
    send_to_rabbitmq(json.dumps(handshake_data))

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
                send_to_rabbitmq(json.dumps(upload_data))
            else:
                print(f"File {file_path} doesn't exist.")
        elif message.startswith("download: "):
            download_command = {
                "type": "download",
                "payload": {"file_name": message[10:], }
            }
            send_to_rabbitmq(json.dumps(download_command))
        else:
            send_to_rabbitmq(json.dumps({
                "type": "message",
                "payload": {"content": message}
            }))

# Start the RabbitMQ listener on a separate thread
threading.Thread(target=listen_to_rabbitmq, daemon=True).start()

send_message()
rabbitmq_connection.close()
