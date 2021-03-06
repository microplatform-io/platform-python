import kombu
import traceback

from kombu.mixins import ConsumerMixin

import logging

logging.getLogger().addHandler(logging.StreamHandler())


class Subscriber(object):
    def subscribe(self, topic, callback):
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

                queues = []  # List of queues that will be passed when we declare worker
                for topic in self.subscriptions.keys():
                    queue = kombu.Queue(
                        name        = self.queue_name + "-" + topic,
                        channel     = channel,
                        durable     = False,
                        auto_delete = True
                    )
                    queue.declare()
                    queue.bind_to('amq.topic', topic)
                    queues.extend([queue])

                worker = KombuWorker(self.connection_manager.connection, queues, self.subscriptions)
                worker.run()

            except Exception, e:
                print "[kombu-subscriber]: connection or channel has been closed, reconnecting: %s, %s" % (e, traceback.format_exc(e), )

                self.connection_manager.reconnect()
