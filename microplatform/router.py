from .connection import get_amqp_connection_from_env
from google.protobuf.message import DecodeError
from Queue import Queue, Empty
from threading import Thread
from urlparse import urlparse

import os
import platform_pb2
import uuid


def get_standard_router(service_name = ''):
    connection = get_amqp_connection_from_env()

    router_uuid = str(uuid.uuid4())

    service_name = service_name or os.environ.get('SERVICE_NAME')

    if service_name:
        subscriber_name = 'router-%s-%s' % (service_name, router_uuid, )
    else:
        subscriber_name = 'router-%s' % (router_uuid, )

    return StandardRouter(connection.get_publisher(), connection.get_subscriber(subscriber_name))


class StandardRouter(object):
    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.topic = str(uuid.uuid4())
        self.pending_requests = {}

        def callback(body, message):
            print "[standard-router] received message: %s" % (message, )

            try:
                response = platform_pb2.Request().FromString(body)

                print "[standard-router] router response: %s" % (response, )

                if response.uuid in self.pending_requests:
                    self.pending_requests[response.uuid].put(response)

                message.ack()

                return True
            except DecodeError, e:
                message.reject()

                print "[standard-router] failed to decode router message: %s" % (e, )

            except Exception, e:
                message.reject()

                print "[standard-router] general processing error: %s" % (e, )

            return False

        self.subscriber.subscribe(self.topic, callback)

        def run_subscriber():
            self.subscriber.run()

        t = Thread(target=run_subscriber)
        t.daemon = True
        t.start()

    def route(self, request, timeout = None):
        request.uuid = str(uuid.uuid4())
        request.routing.route_from._values.append(platform_pb2.Route(uri=self.topic))

        self.pending_requests[request.uuid] = Queue()

        print "ROUTING REQUEST: %s" % (request, )

        payload = request.SerializeToString()

        parsed_uri = urlparse(request.routing.route_to[0].uri)

        print "PARSED URI: %s" % (parsed_uri, )

        self.publisher.publish(parsed_uri.path, payload)

        try:
            return self.pending_requests[request.uuid].get(block=True, timeout=timeout or 2)

        except Empty:
            self.publisher.publish('request.timeout', payload)

            return platform_pb2.Request(
                routing     = platform_pb2.Routing(
                    route_from  = [platform_pb2.Route(uri=self.topic)],
                    route_to    = [platform_pb2.Route(uri='resource:///platform/reply/error')] + request.routing.route_from._values[:-1]
                ),
                context     = request.context,
                payload     = platform_pb2.Error(message="API Request has timed out").SerializeToString()
            )

        finally:
            del self.pending_requests[request.uuid]
