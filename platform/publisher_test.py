import amqptest
import platform_pb2
import unittest

from .publisher import AmqpPublisher

class AmqpPublisherTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = amqptest.MockConnection()
        self.assertEqual(len(self.connection.channels), 0)
        self.publisher = AmqpPublisher(self.connection)
        self.assertEqual(len(self.connection.channels), 0)

    def test_publish(self):
        self.assertEqual(len(self.connection.channels), 0)
        self.publisher.publish('testing', '1234')
        self.assertEqual(len(self.connection.channels), 1)

        channel = self.connection.channels[-1]
        
        self.assertEqual(channel.publishes, [{
            'routing_key'   : 'testing',
            'exchange'      : 'amq.topic',
            'body'          : '1234'
        }])