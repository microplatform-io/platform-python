import pika.exceptions

class Publisher(object):
    def publish(self, topic, body):
        pass

class AmqpPublisher(Publisher):
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.channel = self.connection_manager.channel()

    def publish(self, topic, body):
        # Try a delivery twice, the connection will attempt multiple reconnects automatically
        for i in xrange(2):
            try:
                self.channel.basic_publish(
                    exchange    = 'amq.topic', 
                    routing_key = topic, 
                    body        = body
                )
            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed, pika.exceptions.AMQPConnectionError, ):
                self.reconnect()

    def reconnect(self):
        self.connection_manager.reconnect()
        self.channel = self.connection_manager.channel()