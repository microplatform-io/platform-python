import os
import sys
sys.path.append(os.path.dirname(__file__) + '/../../')

import microplatform

connection = microplatform.get_default_connection()
publisher = microplatform.AmqpPublisher(connection)

documentation_list = microplatform.DocumentationList(
    documentations=[
        microplatform.Documentation(description="microservice 1"),
        microplatform.Documentation(description="microservice 2"),
    ]
)

request = microplatform.Request(
    body    = documentation_list.SerializeToString()
)

publisher.publish('%d_%d' % (microplatform.GET, microplatform.DOCUMENTATION_LIST, ), request.SerializeToString())