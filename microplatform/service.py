from .connection import get_amqp_connection_from_env
from google.protobuf.message import DecodeError
from .subscriber import KombuSubscriber
from .subscriber import PikaSubscriber
import platform_pb2
import traceback

def get_standard_service(queue_name):
    connection_manager = get_amqp_connection_from_env()

    return Service(connection_manager.get_publisher(), connection_manager.get_subscriber(queue_name))

class Service(object):
    class NoHandlersDefined(Exception):
        pass

    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.handlers = {}

    def handle(self, method, resource):
        topic = '%d_%d' % (method, resource, )

        if isinstance(self.subscriber, PikaSubscriber):
            def callback(ch, method, properties, body):
                print "received message: %s" % (method, )
                
                if method.routing_key not in self.handlers:
                    return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

                # TODO(bmoyles0117): Might want to copy the routed message every time to make immutable
                try:
                    routed_message = platform_pb2.RoutedMessage().FromString(body)

                    # Invoke every handler that matches the routing key
                    for handler in self.handlers[method.routing_key]:
                        response = handler(routed_message)

                        if isinstance(response, platform_pb2.RoutedMessage):
                            response.id = routed_message.id

                            self.publisher.publish(routed_message.reply_topic, response.SerializeToString(), mandatory=True)

                except DecodeError, e:
                    print "decode error, failing permanently: %s" % (e, )

                    return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                except Exception, e:
                    if method.redelivered:
                        print "generic error, already redelivered, rejecting: %s\n%s" % (e, traceback.format_exc(e), )

                        return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                    else:
                        print "generic error, requeuing: %s\n%s" % (e, traceback.format_exc(e), )

                        return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

                ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)
                # return self.handle_callback(ch, method, properties, body)

        elif isinstance(self.subscriber, KombuSubscriber):
            def callback(body, message):
                if message.delivery_info['routing_key'] not in self.handlers:
                    return message.reject()

                routed_message = platform_pb2.RoutedMessage().FromString(body)

                # print 'REDELIVERED', message.delivery_info['redelivered']

                # Invoke every handler that matches the routing key
                for handler in self.handlers[message.delivery_info['routing_key']]:
                    response = handler(routed_message)

                    if isinstance(response, platform_pb2.RoutedMessage):
                        response.id = routed_message.id

                        self.publisher.publish(routed_message.reply_topic, response.SerializeToString(), mandatory=True)

                message.ack()

        def decorator(f):
            if topic in self.handlers:
                self.handlers[topic].append(f)
            else:
                self.handlers[topic] = [f]

            self.subscriber.subscribe(topic, callback)

            return f

        return decorator

    def listen(self, topic):
        if isinstance(self.subscriber, PikaSubscriber):
            def callback(ch, method, properties, body):
                print "received message: %s" % (method, )
                
                if method.routing_key not in self.handlers:
                    return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

                try:
                    # Invoke every handler that matches the routing key
                    for handler in self.handlers[method.routing_key]:
                        handler(body)

                except Exception, e:
                    if method.redelivered:
                        print "generic error, already redelivered, rejecting: %s\n%s" % (e, traceback.format_exc(e), )

                        return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                    else:
                        print "generic error, requeuing: %s\n%s" % (e, traceback.format_exc(e), )

                        return ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

                ch.basic_ack(delivery_tag=method.delivery_tag, multiple=True)

        elif isinstance(self.subscriber, KombuSubscriber):
            def callback(body, message):
                if message.delivery_info['routing_key'] not in self.handlers:
                    return message.reject()

                # print 'REDELIVERED', message.delivery_info['redelivered']

                # Invoke every handler that matches the routing key
                for handler in self.handlers[message.delivery_info['routing_key']]:
                    handler(body)

                message.ack()

        def decorator(f):
            if topic in self.handlers:
                self.handlers[topic].append(f)
            else:
                self.handlers[topic] = [f]

            self.subscriber.subscribe(topic, callback)

            return f

        return decorator

    def run(self):
        if not len(self.handlers):
            raise Service.NoHandlersDefined('No handlers have been defined!')

        self.subscriber.run()
