import platform_pb2
import unittest

from .service import Service

class ServiceTestCase(unittest.TestCase):
	def setUp(self):
		self.service = Service()

	def test_handle(self):
		# Initially, no handlers should exist on a service
		self.assertEqual(self.service.handlers, {})

		# Let's just pseudo-wrap a temporary function
		@self.service.handle(platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST)
		def handler_func(request):
			pass

		# Now that we've added a handler, it should exist in the service's handler map
		self.assertEqual(self.service.handlers, {
			'%d_%d' % (platform_pb2.GET, platform_pb2.DOCUMENTATION_LIST, ): [handler_func],
		})