from .connection import get_amqp_connection_from_env
from google.protobuf.message import DecodeError
import platform_pb2


def get_standard_service(queue_name):
    connection_manager = get_amqp_connection_from_env()

    return Service(connection_manager.get_publisher(), connection_manager.get_subscriber(queue_name))


class Courier(object):
    def __init__(self, publisher, route_from):
        self.publisher = publisher
        self.route_from = route_from

    def send(self, request):
        destination = request.routing.route_to[-1]

        request.routing.route_to.remove(destination)
        request.routing.route_from._values = [self.route_from]

        print "PUBLISHING REQUEST", request

        self.publisher.publish(destination.uri, request.SerializeToString())


class Service(object):
    class NoHandlersDefined(Exception):
        pass

    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.handlers = {}

    def generate_callback_decorator(self, topic, callback):
        def decorator(f):
            if topic in self.handlers:
                self.handlers[topic].append(f)
            else:
                self.handlers[topic] = [f]

            self.subscriber.subscribe(topic, callback)

            return f

        return decorator

    def handle(self, path):
        courier = Courier(self.publisher, route_from=platform_pb2.Route(uri=path))

        def callback(body, message):
            if message.delivery_info['routing_key'] not in self.handlers:
                return message.reject()

            try:
                router_request = platform_pb2.Request().FromString(body)

                # Invoke every handler that matches the routing key
                for handler in self.handlers[message.delivery_info['routing_key']]:
                    handler(courier, router_request)

                message.ack()
            except DecodeError, e:
                print "decode error, failing permanently: %s" % (e, )

                return message.reject()

        return self.generate_callback_decorator(path, callback)

    def listen(self, topic):
        def callback(body, message):
            if message.delivery_info['routing_key'] not in self.handlers:
                return message.reject()

            # print 'REDELIVERED', message.delivery_info['redelivered']

            # Invoke every handler that matches the routing key
            for handler in self.handlers[message.delivery_info['routing_key']]:
                handler(body)

            message.ack()

        return self.generate_callback_decorator(topic, callback)

    def run(self):
        if not len(self.handlers):
            raise Service.NoHandlersDefined('No handlers have been defined!')

        self.subscriber.run()
