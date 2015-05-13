import platform_pb2
import unittest

from .service import Service

class MockMethod(object):
    def __init__(self, routing_key):
        self.routing_key = routing_key

class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.service = Service()

    def test_handle(self):
        # Initially, no handlers should exist on a service
        self.assertEqual(self.service.handlers, {})

        handler_storage = {'requests': []}

        # Let's just pseudo-wrap a temporary function
        @self.service.handle(platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST)
        def handler_func(request):
            handler_storage['requests'].append(request)

        # Now that we've added a handler, it should exist in the service's handler map
        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        self.assertEqual(self.service.handlers, {
            routing_key: [handler_func],
        })

        # Let's make sure calling the function still works
        self.assertEqual(handler_storage['requests'], [])
        handler_func(None)
        self.assertEqual(handler_storage['requests'], [None])

        # Now let's make sure calling the callback through the service works
        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        self.service.handle_callback(None, MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(handler_storage['requests']), 2)

        handled_request = handler_storage['requests'][-1]
        self.assertEqual(request.method, handled_request.method)
        self.assertEqual(request.resource, handled_request.resource)
        self.assertEqual(request.body, handled_request.body)

        # Calling the service for a routing_key that doesn't match should not invoke the handler
        self.service.handle_callback(None, MockMethod('bad-routing-key'), None, request.SerializeToString())
        self.assertEqual(len(handler_storage['requests']), 2) # Should remain at 2 requests