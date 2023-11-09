import pika

def receive_messages_from_rabbitmq():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection_parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f"Received {body}")

    channel.queue_declare(queue='my_queue')
    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# Example use:
receive_messages_from_rabbitmq()
