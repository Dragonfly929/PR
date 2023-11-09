import pika

# Initialize a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue for sending URLs
channel.queue_declare(queue='url_queue', durable=True)

def send_url_to_queue(url):
    # Send the URL to the queue
    channel.basic_publish(exchange='', routing_key='url_queue', body=url)

# Read URLs from a file or any other source
with open("parsed_product_urls.json", 'r') as file:
    urls = file.read().splitlines()

# Send each URL to the queue
for url in urls:
    send_url_to_queue(url)

# Close the RabbitMQ connection
connection.close()
