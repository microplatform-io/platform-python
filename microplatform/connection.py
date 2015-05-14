import os
import pika

class AmqpConnection(object):
    def __init__(self, host, port, user, password):
        connection_params = pika.ConnectionParameters(
            host        = host,
            port        = int(port),
            credentials = pika.PlainCredentials(user, password)
        )

        self.connection = pika.BlockingConnection(connection_params)

    def channel(self):
        return self.connection.channel()

def get_default_connection():
    return AmqpConnection(
        host        = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', '127.0.0.1'),
        port        = os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', 5672),
        user        = os.environ.get('RABBITMQ_USER', 'guest'),
        password    = os.environ.get('RABBITMQ_PASS', 'guest')
    )