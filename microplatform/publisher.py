class Publisher(object):
    def publish(self, topic, body):
        pass

class AmqpPublisher(Publisher):
    def __init__(self, connection):
        self.connection = connection

    def publish(self, topic, body):
        channel = self.connection.channel()
        print "PUBLISHED", channel.basic_publish(
            exchange    = 'amq.topic', 
            routing_key = topic, 
            body        = body
        )