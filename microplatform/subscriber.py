import kombu
import pika.exceptions
import traceback

from kombu.mixins import ConsumerMixin

import logging

logging.getLogger().addHandler(logging.StreamHandler())


class Subscriber(object):
    def subscribe(self, topic, body):
        pass


class KombuException(Exception):
    pass


class KombuWorker(ConsumerMixin):
    def __init__(self, connection, queues, subscriptions):
        self.connection = connection
        self.queues = queues
        self.subscriptions = subscriptions

    def get_consumers(self, Consumer, channel):
        def on_message(message):
            for callback in self.subscriptions.get(message.delivery_info['routing_key'], []):
                callback(message.body, message)

        return [Consumer(auto_declare=True, queues=self.queues, on_message=on_message)]

    def on_connection_error(self, exc, interval):
        raise KombuException("Our connection has expired, let's bubble it up: %s" % (exc, ))


class KombuSubscriber(Subscriber):
    def __init__(self, connection_manager, queue_name):
        self.connection_manager = connection_manager
        self.queue_name = queue_name
        self.subscriptions = {}

    def subscribe(self, topic, callback):
        print "[kombu-subscriber]: subscribed to %s with %s" % (topic, callback, )

        if topic in self.subscriptions:
            self.subscriptions[topic].append(callback)
        else:
            self.subscriptions[topic] = [callback]

    def run(self):
        while True:
            try:
                print "[kombu-subscriber]: generating channel and declaring queue", self.connection_manager.connection

                channel = self.connection_manager.channel()

                print "[kombu-subscriber]: subscribing topics"

                queue = kombu.Queue(
                    name        = self.queue_name,
                    channel     = channel,
                    durable     = False,
                    auto_delete = True
                )
                queue.declare()

                for topic in self.subscriptions.keys():
                    queue.bind_to('amq.topic', topic)

                worker = KombuWorker(self.connection_manager.connection, [queue], self.subscriptions)
                worker.run()

            except Exception, e:
                print "[kombu-subscriber]: connection or channel has been closed, reconnecting: %s, %s" % (e, traceback.format_exc(e), )

                self.connection_manager.reconnect()


class PikaSubscriber(Subscriber):
    def __init__(self, connection_manager, queue_name):
        self.connection_manager = connection_manager
        self.queue_name = queue_name
        self.subscriptions = []

    def subscribe(self, topic, callback):
        print "[pika-subscriber]: subscribed to %s with %s" % (topic, callback, )

        self.subscriptions.append((topic, callback, ))

    def run(self):
        while True:
            try:
                print "[pika-subscriber]: generating channel and declaring queue"

                channel = self.connection_manager.channel()
                channel.queue_declare(queue=self.queue_name, durable=False, auto_delete=True)

                print "[pika-subscriber]: subscribing topics and callbacks"

                for topic, callback in self.subscriptions:
                    channel.queue_bind(exchange='amq.topic', queue=self.queue_name, routing_key=topic)
                    channel.basic_consume(consumer_callback=callback, queue=self.queue_name, no_ack=False)

                print "[pika-subscriber]: consuming"

                channel.start_consuming()
            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError, ):
                print "[pika-subscriber]: connection or channel has been closed, reconnecting"

                self.connection_manager.reconnect()
