import pika

def send_message_to_rabbitmq(message):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection_parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue='my_queue')
    channel.basic_publish(exchange='', routing_key='my_queue', body=message)

    connection.close()

# Example use:
send_message_to_rabbitmq('Hello RabbitMQ!')
