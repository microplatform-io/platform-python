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

        self.reconnect()

    def channel(self):
        return self.connection.channel()

    def reconnect(self):
        for i in xrange(50):
            try:
                self.connection = pika.BlockingConnection(self.connection_params)
            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError, ):
                print "failed to reconnect, trying again in %s seconds" % (i % 5, )
                time.sleep(i % 5)
                pass

def get_amqp_connection_from_env():
    return AmqpConnectionManager(
        host        = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', '127.0.0.1'),
        port        = os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', 5672),
        user        = os.environ.get('RABBITMQ_USER', 'guest'),
        password    = os.environ.get('RABBITMQ_PASS', 'guest')
    )