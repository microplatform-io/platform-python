class Subscriber(object):
    def subscribe(self, topic, body):
        pass

class AmqpSubscriber(Subscriber):
    def __init__(self, connection, queue_name):
        self.connection = connection
        self.queue_name = queue_name

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=False, auto_delete=True)

    def subscribe(self, topic, callback):
        print "amqp subscriber: subscribed to %s with %s" % (topic, callback, )
       
        self.channel.queue_bind(exchange='amq.topic', queue=self.queue_name, routing_key=topic)
        self.channel.basic_consume(consumer_callback=callback, queue=self.queue_name, no_ack=False)

    def run(self):
        print "amqp subscriber: consuming..."

        self.channel.start_consuming()