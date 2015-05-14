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