import os
import pika
import pika.exceptions
import time

class AmqpConnectionManager(object):
    def __init__(self, host, port, user, password):
        self.connection_params = pika.ConnectionParameters(
            host                = host,
            port                = int(port),
            credentials         = pika.PlainCredentials(user, password),
            connection_attempts = 1,
            retry_delay         = 0,
            socket_timeout      = 1
        )

        self.event_handlers = {}

        self.reconnect()

    def channel(self):
        return self.connection.channel()

    def on(self, event, handler):
        if event not in self.event_handlers:
            self.event_handlers[event] = []

        self.event_handlers[event].append(handler)

    def reconnect(self):
        print "[amqp-connection-manager] attempting to create a connection"

        for i in xrange(50):
            try:
                self.connection = pika.BlockingConnection(self.connection_params)

                self.trigger('connect')

                print "[amqp-connection-manager] connected on attempt %s" % (i, )

                break

            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError, ):
                print "[amqp-connection-manager] failed to reconnect, trying again in %s seconds" % (i % 5, )
                time.sleep(i % 5)
                pass

    def trigger(self, event):
        for event_handler in self.event_handlers.get(event, []):
            event_handler()

def get_amqp_connection_from_env():
    return AmqpConnectionManager(
        host        = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', '127.0.0.1'),
        port        = os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', 5672),
        user        = os.environ.get('RABBITMQ_USER', 'guest'),
        password    = os.environ.get('RABBITMQ_PASS', 'guest')
    )