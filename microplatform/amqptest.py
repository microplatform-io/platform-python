class MockConnection(object):
    def __init__(self):
        self.closed = False
        self.channels = []

    def channel(self):
        self.channels.append(MockChannel(self))

        return self.channels[-1]

    def close(self):
        self.closed = True


class MockChannel(object):
    def __init__(self, connection):
        self.connection = connection
        self.exchanges = []
        self.publishes = []
        self.queues = []
        self.binds = []
        self.consumes = []
        self.started_consuming = False
        self.basic_acks = []
        self.basic_rejects = []

    def basic_ack(self, **kwargs):
        self.basic_acks.append(kwargs)

    def basic_consume(self, **kwargs):
        self.consumes.append(kwargs)

    def basic_publish(self, **kwargs):
        self.publishes.append(kwargs)

    def basic_reject(self, **kwargs):
        self.basic_rejects.append(kwargs)

    def exchange_declare(self, **kwargs):
        self.exchanges.append(kwargs)

    def queue_bind(self, **kwargs):
        self.binds.append(kwargs)

    def queue_declare(self, **kwargs):
        self.queues.append(kwargs)

    def start_consuming(self):
        self.started_consuming = True
