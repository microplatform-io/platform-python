import os
import sys
sys.path.append(os.path.dirname(__file__) + '/../../')

import microplatform

connection = microplatform.get_default_connection()
publisher = microplatform.AmqpPublisher(connection)

routing_key = '%d_%d' % (microplatform.GET, microplatform.DOCUMENTATION_LIST, )

publisher.publish(routing_key, 'abc')