from .connection import get_default_connection
from google.protobuf.message import DecodeError
from .publisher import AmqpPublisher
from .subscriber import AmqpSubscriber
import platform_pb2

def get_default_service(queue_name):
    connection = get_default_connection()

    return Service(AmqpPublisher(connection), AmqpSubscriber(connection, queue_name))

class Service(object):
    class NoHandlersDefined(Exception):
        pass

    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.handlers = {}

    def handle(self, method, resource):
        def callback(ch, method, properties, body):
            return self.handle_callback(ch, method, properties, body)

        print "subscribing to: %d_%d" % (method, resource, )

        def decorator(f):
            topic = '%d_%d' % (method, resource, )

            if topic in self.handlers:
                self.handlers[topic].append(f)
            else:
                self.handlers[topic] = [f]

            self.subscriber.subscribe(topic, callback)

            return f

        return decorator

    def handle_callback(self, ch, method, properties, body):
        print "received message: %s" % (method, )
        
        if method.routing_key not in self.handlers:
            return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

        # TODO(bmoyles0117): Might want to copy the request every time to make immutable
        try:
            request = platform_pb2.Request().FromString(body)

            # Invoke every handler that matches the routing key
            [handler(request) for handler in self.handlers[method.routing_key]]
        except DecodeError, e:
            print "decode error, failing permanently: %s" % (e, )

            return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        except Exception, e:
            print "generic error, requeuing: %s" % (e, )

            return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)

    def run(self):
        if not len(self.handlers):
            raise Service.NoHandlersDefined('No handlers have been defined!')

        self.subscriber.run()