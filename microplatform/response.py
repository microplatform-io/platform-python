class Response(object):
    def __init__(self, method, resource, protobuf):
        self.method = method
        self.resource = resource
        self.protobuf = protobuf