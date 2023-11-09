import pika
import requests
from bs4 import BeautifulSoup
import json
from homework import extract_product_details
# Initialize a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same queue for receiving URLs
channel.queue_declare(queue='url_queue', durable=True)


def callback(ch, method, properties, body):
    url = body.decode('utf-8')
    product_details = extract_product_details(url)

    # Modify this part to save the data as needed
    if product_details:
        with open("product_data.json", 'a', encoding='utf-8') as json_file:
            json.dump(product_details, json_file, ensure_ascii=False, indent=4)

    # Acknowledge that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages from the queue
channel.basic_qos(prefetch_count=1)  # Process one message at a time
channel.basic_consume(queue='url_queue', on_message_callback=callback)

print('Consumer is waiting for messages. To exit press CTRL+C')
channel.start_consuming()
