from .connection import get_amqp_connection_from_env
from google.protobuf.message import DecodeError
from Queue import Queue, Empty
from .subscriber import KombuSubscriber
from .subscriber import PikaSubscriber
from threading import Thread

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

        if isinstance(subscriber, PikaSubscriber):
            def callback(ch, method, properties, body):
                print "[standard-router] received message: %s" % (method, )

                try:
                    routed_message = platform_pb2.RoutedMessage().FromString(body)

                    print "[standard-router] routed message: %s" % (routed_message, )

                    if routed_message.id in self.pending_requests:
                        self.pending_requests[routed_message.id].put(routed_message)

                    return ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)
                except DecodeError, e:
                    print "[standard-router] failed to decode routed message: %s" % (e, )

                    return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                except Exception, e:
                    print "[standard-router] general processing error: %s" % (e, )

                    return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        elif isinstance(subscriber, KombuSubscriber):
            def callback(body, message):
                print "[standard-router] received message: %s" % (message, )

                try:
                    routed_message = platform_pb2.RoutedMessage().FromString(body)

                    print "[standard-router] routed message: %s" % (routed_message, )

                    if routed_message.id in self.pending_requests:
                        self.pending_requests[routed_message.id].put(routed_message)

                    message.ack()

                    return True
                except DecodeError, e:
                    message.reject()

                    print "[standard-router] failed to decode routed message: %s" % (e, )

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

    def route(self, routed_message, timeout = None):
        routed_message.id = str(uuid.uuid4())
        routed_message.reply_topic = self.topic

        self.pending_requests[routed_message.id] = Queue()

        # print "ROUTING MESSAGE: %s" % (routed_message, )

        payload = routed_message.SerializeToString()

        self.publisher.publish('%d_%d' % (routed_message.method, routed_message.resource, ), payload)

        try:
            return self.pending_requests[routed_message.id].get(block=True, timeout=timeout or 2)

        except Empty:
            self.publisher.publish('request.timeout', payload)

            return platform_pb2.RoutedMessage(
                method      = platform_pb2.REPLY,
                resource    = platform_pb2.ERROR,
                body        = platform_pb2.Error(message="API Request has timed out").SerializeToString()
            )

        finally:
            del self.pending_requests[routed_message.id]
