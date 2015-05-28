from .connection import get_amqp_connection_from_env
from google.protobuf.message import DecodeError
from .publisher import AmqpPublisher
from Queue import Queue, Empty
from .subscriber import AmqpSubscriber
from threading import Thread

import platform_pb2
import uuid

def get_standard_router():
    connection = get_amqp_connection_from_env()

    return StandardRouter(AmqpPublisher(connection), AmqpSubscriber(connection, 'router-' + str(uuid.uuid4())))

class StandardRouter(object):
    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.topic = str(uuid.uuid4())
        self.pending_requests = {}

        def callback(ch, method, properties, body):
            print "[standard-router] received message: %s" % (method, )

            try:
                routed_message = platform_pb2.RoutedMessage().FromString(body)

                if routed_message.id in self.pending_requests:
                    self.pending_requests[routed_message.id].put(routed_message)

                return ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)
            except DecodeError, e:
                print "[standard-router] failed to decode routed message: %s" % (e, )

                return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            except Exception, e:
                print "[standard-router] general processing error: %s" % (e, )

                return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

        self.subscriber.subscribe(self.topic, callback)

        def run_subscriber():
            self.subscriber.run()

        t = Thread(target=run_subscriber)
        t.daemon = True
        t.start()

    def route(self, routed_message, timeout = 2):
        routed_message.id = str(uuid.uuid4())
        routed_message.reply_topic = self.topic

        self.pending_requests[routed_message.id] = Queue()

        # print "ROUTING MESSAGE: %s" % (routed_message, )

        self.publisher.publish('%d_%d' % (routed_message.method, routed_message.resource, ), routed_message.SerializeToString())

        try:
            return self.pending_requests[routed_message.id].get(block=True, timeout=timeout)

        except Empty:
            return platform_pb2.RoutedMessage(
                method      = platform_pb2.REPLY,
                resource    = platform_pb2.ERROR,
                body        = platform_pb2.Error(message="API Request has timed out").SerializeToString()
            )

        finally:
            del self.pending_requests[routed_message.id]