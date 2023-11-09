import pika

# Define RabbitMQ server connection parameters
credentials = pika.PlainCredentials('username', 'password')  # default is guest/guest
connection_parameters = pika.ConnectionParameters('localhost',  # Server address
                                                  5672,         # Server port
                                                  '/',          # Virtual host, default is '/'
                                                  credentials)

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()  # Create a new channel
