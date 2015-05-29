class Publisher(object):
    def publish(self, topic, body):
        pass

class AmqpPublisher(Publisher):
    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.channel()

    def publish(self, topic, body):
        self.channel.basic_publish(
            exchange    = 'amq.topic', 
            routing_key = topic, 
            body        = body
        )