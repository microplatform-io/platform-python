import amqptest
import platform_pb2
import unittest

from .publisher import AmqpPublisher
from .service import Service
from .subscriber import AmqpSubscriber

class MockMethod(object):
    def __init__(self, routing_key):
        self.routing_key = routing_key

class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.connection = amqptest.MockConnection()
        self.publisher = AmqpPublisher(self.connection)

        # The subscriber should create a channel
        self.assertEqual(len(self.connection.channels), 0)
        self.subscriber = AmqpSubscriber(self.connection, 'test-queue')
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 0)
        
        # Creating the service should leave everything as it was before
        self.service = Service(self.publisher, self.subscriber)
        self.assertEqual(self.service.publisher, self.publisher)
        self.assertEqual(self.service.subscriber, self.subscriber)
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 0)

    def test_handle(self):
        # Initially, no handlers should exist on a service
        self.assertEqual(self.service.handlers, {})

        handler_storage = {'requests': []}

        # Let's just pseudo-wrap a temporary function
        @self.service.handle(platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST)
        def handler_func(request):
            handler_storage['requests'].append(request)

        # After adding the handler decorator, we should see the bind count go up
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 1)

        # Now that we've added a handler, it should exist in the service's handler map
        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        self.assertEqual(self.service.handlers, {
            routing_key: [handler_func],
        })

        # Let's make sure calling the function still works
        self.assertEqual(len(handler_storage['requests']), 0)
        handler_func(None)
        self.assertEqual(len(handler_storage['requests']), 1)

    def test_handle_callback(self):
        # Initially, no handlers should exist on a service
        self.assertEqual(self.service.handlers, {})

        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        handler_storage = {'requests': []}

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        # An initial callback that has not been registered should not trigger the function
        self.assertEqual(len(handler_storage['requests']), 0)
        self.service.handle_callback(None, MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(handler_storage['requests']), 0)

        # Now let's register the handler, and call it again
        self.service.handle(platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST)(lambda request: handler_storage['requests'].append(request))

        self.assertEqual(len(handler_storage['requests']), 0)
        self.service.handle_callback(None, MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(handler_storage['requests']), 1)