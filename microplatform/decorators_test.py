import unittest

from .decorators import extract_request
from google.protobuf.message import DecodeError
from .platform_pb2 import ERROR
from .platform_pb2 import REPLY
from .platform_pb2 import Request
from .platform_pb2 import RoutedMessage

class DecoratorsTestCase(unittest.TestCase):
    def test_extract_request_invalid(self):
        routed_message = RoutedMessage(
            body    = 'invalid-body'
        )

        def handler(routed_message, microplatform_request):
            pass

        with self.assertRaises(DecodeError):
            extract_request(handler)(routed_message)

    def test_extract_request_valid(self):
        routed_message = RoutedMessage(
            body    = Request(body='valid-body').SerializeToString()
        )

        handler_data = {
            'microplatform_request' : None
        }

        def handler(routed_message, microplatform_request):
            handler_data['microplatform_request'] = microplatform_request

        extract_request(handler)(routed_message)

        self.assertIsNotNone(handler_data['microplatform_request'])

if __name__ == '__main__':
    unittest.main()