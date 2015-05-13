import platform_pb2
import unittest

from .publisher import AmqpPublisher

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

	def basic_publish(self, **kwargs):
		self.publishes.append(kwargs)

	def exchange_declare(self, **kwargs):
		self.exchanges.append(kwargs)

class AmqpPublisherTestCase(unittest.TestCase):
	def setUp(self):
		self.connection = MockConnection()
		self.assertEqual(len(self.connection.channels), 0)
		self.publisher = AmqpPublisher(self.connection)
		self.assertEqual(len(self.connection.channels), 0)

	def test_publish(self):
		self.assertEqual(len(self.connection.channels), 0)
		self.publisher.publish('testing', '1234')
		self.assertEqual(len(self.connection.channels), 1)

		channel = self.connection.channels[-1]
		
		self.assertEqual(channel.publishes, [{
			'routing_key'	: 'testing',
			'exchange'		: 'amq.topic',
			'body'			: '1234'
		}])