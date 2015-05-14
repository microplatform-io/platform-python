import platform_pb2

class Service(object):
    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.handlers = {}

    def handle(self, method, resource):
        # def callback(ch, method, properties, body):
        #     return self.handle_callback(ch, method, properties, body)

        def decorator(f):
            topic = '%d_%d' % (method, resource, )

            if topic in self.handlers:
                self.handlers[topic].append(f)
            else:
                self.handlers[topic] = [f]

            self.subscriber.subscribe(topic, self.handle_callback)

            return f

        return decorator

    def handle_callback(self, ch, method, properties, body):
        if method.routing_key not in self.handlers:
            return

        # TODO(bmoyles0117): Might want to copy the request every time to make immutable
        request = platform_pb2.Request().FromString(body)

        # Invoke every handler that matches the routing key
        [handler(request) for handler in self.handlers[method.routing_key]]