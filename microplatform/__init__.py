from .connection import get_amqp_connection_from_env
from google.protobuf.message import DecodeError
from .platform_pb2 import *
# from .publisher import AmqpPublisher
from .router import StandardRouter, get_standard_router
from .service import Service, get_standard_service
# from .subscriber import AmqpSubscriber

ORGANIZATION = 'platform'

def basic_event(organization, method, resource, payload):
    return Event(
        organization    = organization,
        method          = method,
        resource        = resource,
        payload         = payload
    )