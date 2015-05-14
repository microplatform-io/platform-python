import os
import sys
sys.path.append(os.path.dirname(__file__) + '/../../')

import microplatform

connection = microplatform.get_default_connection()
publisher = microplatform.AmqpPublisher(connection)
service = microplatform.Service(publisher, microplatform.AmqpSubscriber(connection, 'testing'))

@service.handle(microplatform.GET, microplatform.DOCUMENTATION_LIST)
def get_documentation(request):
    print request

service.run()