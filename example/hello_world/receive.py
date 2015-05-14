import os
import sys
sys.path.append(os.path.dirname(__file__) + '/../../')

import microplatform

connection = microplatform.AmqpConnection(
    host        = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', '127.0.0.1'),
    port        = os.environ.get('RABBITMQ_PORT_5672_TCP_PORT', 5672),
    user        = os.environ.get('RABBITMQ_USER', 'guest'),
    password    = os.environ.get('RABBITMQ_PASS', 'guest')
)

publisher = microplatform.AmqpPublisher(connection)
service = microplatform.Service(publisher, microplatform.AmqpSubscriber(connection, 'testing'))

@service.handle(microplatform.GET, microplatform.DOCUMENTATION_LIST)
def get_documentation(request):
    print request

service.run()