class Service(object):
    def __init__(self):
        self.handlers = {}

    def handle(self, method, resource):
        def decorator(f):
            topic = '%d_%d' % (method, resource, )

            if topic in self.handlers:
                self.handlers[topic].append(f)
            else:
                self.handlers[topic] = [f]

            return f

        return decorator