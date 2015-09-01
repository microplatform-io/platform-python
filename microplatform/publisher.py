from amqp import Message


class Publisher(object):
    def publish(self, topic, body):
        pass


class KombuPublisher(Publisher):
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def publish(self, topic, body, mandatory = False):
        # Try a delivery twice, the connection will attempt multiple reconnects automatically
        for i in xrange(2):
            print "[amqp-publisher] publishing {topic:%s, mandatory: %s}" % (topic, mandatory, )

            try:
                channel = self.connection_manager.channel()
                result = channel.basic_publish(Message(body=body, content_encoding='binary'), exchange='amq.topic', routing_key=topic)
                channel.close()

                print "[amqp-publisher] published: %s" % (result, )

                break

            except (Exception, ), e:
                print "[amqp-publisher] failed to publish, reconnecting: exception %s" % (e, )

                self.connection_manager.reconnect()
