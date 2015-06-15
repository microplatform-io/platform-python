import kombu
import os
import pika
import pika.exceptions
import time

from .publisher import KombuPublisher
from .publisher import PikaPublisher
from .subscriber import KombuSubscriber
from .subscriber import PikaSubscriber

class KombuConnectionManager(object):
    def __init__(self, host, port, user, password):
        self.connection_params = {
            'hostname'  : host,
            'port'      : port,
            'userid'    : user,
            'password'  : password
        }

        self.event_handlers = {}

        self.reconnect()

    def channel(self):
        connection = self.connection_pool.acquire()
        channel = connection.channel()
        connection.release()

        return channel

    def get_publisher(self):
        return KombuPublisher(self)

    def get_subscriber(self, queue_name):
        return KombuSubscriber(self, queue_name)

    def on(self, event, handler):
        if event not in self.event_handlers:
            self.event_handlers[event] = []

        self.event_handlers[event].append(handler)

    def reconnect(self):
        print "[kombu-connection-manager] attempting to create a connection: %s" % (self.connection_params, )

        for i in xrange(50):
            try:
                self.connection = kombu.Connection(**self.connection_params)
                self.connection_pool = self.connection.Pool(limit=2, preload=2)

                self.trigger('connect')

                print "[kombu-connection-manager] connected on attempt %s" % (i, )

                break

            except Exception, e:
                print "[kombu-connection-manager] failed to reconnect %s, trying again in %s seconds" % (e, i % 5, )
                time.sleep(i % 5)

    def trigger(self, event):
        for event_handler in self.event_handlers.get(event, []):
            event_handler()

class PikaConnectionManager(object):
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

    def get_publisher(self):
        return PikaPublisher(self)

    def get_subscriber(self, queue_name):
        return PikaSubscriber(self, queue_name)

    def on(self, event, handler):
        if event not in self.event_handlers:
            self.event_handlers[event] = []

        self.event_handlers[event].append(handler)

    def reconnect(self):
        print "[pika-connection-manager] attempting to create a connection"

        for i in xrange(50):
            try:
                self.connection = pika.BlockingConnection(self.connection_params)

                self.trigger('connect')

                print "[pika-connection-manager] connected on attempt %s" % (i, )

                break

            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError, ):
                print "[pika-connection-manager] failed to reconnect, trying again in %s seconds" % (i % 5, )
                time.sleep(i % 5)
                pass

    def trigger(self, event):
        for event_handler in self.event_handlers.get(event, []):
            event_handler()

def get_amqp_connection_from_env():
    return KombuConnectionManager(
        host        = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', '127.0.0.1'),
        port        = os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', 5672),
        user        = os.environ.get('RABBITMQ_USER', 'guest'),
        password    = os.environ.get('RABBITMQ_PASS', 'guest')
    )