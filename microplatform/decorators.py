from .platform_pb2 import Request


def extract_request(f):
    def decorator(routed_message):
        microplatform_request = Request().FromString(routed_message.body)

        return f(routed_message, microplatform_request=microplatform_request)

    return decorator
