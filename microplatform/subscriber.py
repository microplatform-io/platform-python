import pika.exceptions

class Subscriber(object):
    def subscribe(self, topic, body):
        pass

class AmqpSubscriber(Subscriber):
    def __init__(self, connection_manager, queue_name):
        self.connection_manager = connection_manager
        self.queue_name = queue_name
        self.subscriptions = []

    def subscribe(self, topic, callback):
        print "amqp subscriber: subscribed to %s with %s" % (topic, callback, )

        self.subscriptions.append((topic, callback, ))

    def run(self):
        while True:
            try:
                print "[amqp-subscriber]: generating channel and declaring queue"

                channel = self.connection_manager.channel()
                channel.queue_declare(queue=self.queue_name, durable=False, auto_delete=True)

                print "[amqp-subscriber]: subscribing topics and callbacks"

                for topic, callback in self.subscriptions:
                    channel.queue_bind(exchange='amq.topic', queue=self.queue_name, routing_key=topic)
                    channel.basic_consume(consumer_callback=callback, queue=self.queue_name, no_ack=False)

                print "[amqp-subscriber]: consuming"

                channel.start_consuming()
            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError, ):
                print "[amqp-subscriber]: connection or channel has been closed, reconnecting"

                self.connection_manager.reconnect()
