import amqptest
import platform_pb2
import unittest

from google.protobuf.message import DecodeError
from .publisher import AmqpPublisher
from .response import Response
from .service import Service
from .subscriber import AmqpSubscriber

class MockMethod(object):
    def __init__(self, routing_key):
        self.routing_key = routing_key
        self.delivery_tag = 1

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

        # Initially, no handlers should exist on a service
        self.assertEqual(self.service.handlers, {})

    def test_handle(self):
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

    def test_handle_callback_unregistered(self):
        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        # An initial callback that has not been registered should not trigger the function
        self.service.handle_callback(self.connection.channels[0], MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(self.connection.channels[0].basic_acks), 0)
        self.assertEqual(len(self.connection.channels[0].basic_rejects), 1)
        self.assertEqual(len(self.connection.channels), 1)

    def test_handle_callback_registered(self):
        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        handler_storage = {'requests': []}

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        def callback(request):
            handler_storage['requests'].append(request)

        self.service.handle(platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST)(callback)

        self.assertEqual(len(handler_storage['requests']), 0)
        self.service.handle_callback(self.connection.channels[0], MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(handler_storage['requests']), 1)
        self.assertEqual(len(self.connection.channels[0].basic_acks), 1)
        self.assertEqual(len(self.connection.channels[0].basic_rejects), 0)
        self.assertEqual(len(self.connection.channels), 1)

    def test_handle_callback_invalid_payload(self):
        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        self.service.handle_callback(self.connection.channels[0], MockMethod(routing_key), None, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.assertEqual(len(self.connection.channels[0].basic_acks), 0)
        self.assertEqual(len(self.connection.channels[0].basic_rejects), 1)
        self.assertEqual(len(self.connection.channels), 1)

    def test_handle_callback_exception(self):
        routing_key = '%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, )

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        def callback(request):
            raise Exception("throwing exception")

        self.service.handle(platform_pb2.GET, 3)(callback)

        self.service.handle_callback(self.connection.channels[0], MockMethod("%d_%d" % (platform_pb2.GET, 3, )), None, request.SerializeToString())
        self.assertEqual(len(self.connection.channels[0].basic_acks), 0)
        self.assertEqual(len(self.connection.channels[0].basic_rejects), 1)
        self.assertEqual(len(self.connection.channels), 1)

        # Last reject should be a requeue
        self.assertEqual(self.connection.channels[0].basic_rejects[-1]['requeue'], True)

    def test_handle_callback_decode_error(self):
        routing_key = '%d_4' % (platform_pb2.GET, )

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        def callback(request):
            raise DecodeError("psuedo decode error")

        self.service.handle(platform_pb2.GET, 4)(callback)

        self.service.handle_callback(self.connection.channels[0], MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(self.connection.channels[0].basic_acks), 0)
        self.assertEqual(len(self.connection.channels[0].basic_rejects), 1)
        self.assertEqual(len(self.connection.channels), 1)

        # Last reject should be a requeue
        self.assertEqual(self.connection.channels[0].basic_rejects[-1]['requeue'], False)

    def test_handle_callback_with_platform_response(self):
        routing_key = '%d_4' % (platform_pb2.GET, )

        request = platform_pb2.Request(
            method      = platform_pb2.GET,
            resource    = platform_pb2.DOCUMENTATION_LIST,
            body        = 'hello'
        )

        def callback(request):
            return Response(platform_pb2.REPLY, platform_pb2.DOCUMENTATION_LIST, platform_pb2.DocumentationList(
                documentations=[platform_pb2.Documentation(description='microservice 1')]
            ))

        self.service.handle(platform_pb2.GET, 4)(callback)

        self.service.handle_callback(self.connection.channels[0], MockMethod(routing_key), None, request.SerializeToString())
        self.assertEqual(len(self.connection.channels[0].basic_acks), 1)
        self.assertEqual(len(self.connection.channels[0].basic_rejects), 0)
        # The publish should have resulted in an extra channel
        self.assertEqual(len(self.connection.channels), 2)
        self.assertEqual(len(self.connection.channels[1].publishes), 1)

        body = platform_pb2.DocumentationList(
            documentations=[platform_pb2.Documentation(description='microservice 1')]
        ).SerializeToString()

        self.assertEqual(self.connection.channels[1].publishes[0], {
            'exchange'      : 'amq.topic',
            'routing_key'   : '%d_%d' % (platform_pb2.REPLY, platform_pb2.DOCUMENTATION_LIST, ),
            'body'          : body
        })

    def test_run(self):
        # Running a service without any handlers should raise an exception
        with self.assertRaises(Service.NoHandlersDefined):
            self.service.run()

        self.service.handle(platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST)(lambda request: request)
        self.assertEqual(len(self.connection.channels), 1)
        self.assertEqual(len(self.connection.channels[0].queues), 1)
        self.assertEqual(len(self.connection.channels[0].binds), 1)
        self.assertEqual(self.connection.channels[0].started_consuming, False)

        self.service.run()

        self.assertEqual(self.connection.channels[0].started_consuming, True)