from .platform_pb2 import Request

def extract_request(f):
    def decorator(routed_message):
        platform_request = Request().FromString(routed_message.body)

        return f(routed_message, platform_request=platform_request)

    return decorator