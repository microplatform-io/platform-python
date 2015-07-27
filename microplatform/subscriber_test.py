import amqptest
import unittest

from .subscriber import AmqpSubscriber


class AmqpSubscriberTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = amqptest.MockConnection()
        self.assertEqual(len(self.connection.channels), 0)
        self.queue_name = 'testing-queue-name'
        self.subscriber = AmqpSubscriber(self.connection, self.queue_name)
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 0)
        self.assertEqual(len(self.connection.channels[0].consumes), 0)

    def test_subscribe(self):
        subscriber_storage = {'callbacks': []}

        def callback(**kwargs):
            subscriber_storage['callbacks'].append(kwargs)

        # AMQP Subscriber only creates one channel for all subscriptions
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 0)
        self.assertEqual(len(self.connection.channels[0].consumes), 0)
        self.subscriber.subscribe('first', callback)
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 1)
        self.assertEqual(len(self.connection.channels[0].consumes), 1)

        self.assertEqual(self.connection.channels[0].queues, [{
            'queue'         : self.queue_name,
            'durable'       : False,
            'auto_delete'   : True
        }])

        self.assertEqual(self.connection.channels[0].binds, [{
            'routing_key'   : 'first',
            'exchange'      : 'amq.topic',
            'queue'         : self.queue_name
        }])

        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 1)
        self.assertEqual(len(self.connection.channels[0].consumes), 1)
        self.subscriber.subscribe('second', callback)
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 2)
        self.assertEqual(len(self.connection.channels[0].consumes), 2)

        self.assertEqual(self.connection.channels[0].queues, [{
            'queue'         : self.queue_name,
            'durable'       : False,
            'auto_delete'   : True
        }])

        self.assertEqual(self.connection.channels[0].binds, [{
            'routing_key'   : 'first',
            'exchange'      : 'amq.topic',
            'queue'         : self.queue_name
        }, {
            'routing_key'   : 'second',
            'exchange'      : 'amq.topic',
            'queue'         : self.queue_name
        }])
