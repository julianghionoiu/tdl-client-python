import re

class RemoteJmxQueue(object):
    def __init__(self, jolokia_session, broker_name, queue_name):
        self.name = queue_name
        self.jolokia_session = jolokia_session
        self.queue_bean = (
            "org.apache.activemq:type=Broker,brokerName={},"
            "destinationType=Queue,destinationName={}"
        ).format(broker_name, queue_name)

    def get_name(self):
        return self.name

    def send_text_message(self, request):
        operation = {
            'type': 'exec',
            'mbean': self.queue_bean,
            'operation': 'sendTextMessage(java.lang.String)',
            'arguments': [request]
        }
        self.jolokia_session.request(operation)

    def get_size(self):
        attribute = {
            'type': 'read',
            'mbean': self.queue_bean,
            'attribute': 'QueueSize',
        }
        return self.jolokia_session.request(attribute)

    def get_message_contents(self):

        operation = {
            'type': 'exec',
            'mbean': self.queue_bean,
            'operation': 'browse()',
        }
        result = self.jolokia_session.request(operation)
        if 'Text' in result[0]:
            return [r['Text'] for r in result]
        else:
            return [self.bytearray_to_string(r) for r in result]

    def bytearray_to_string(self, r):
        result = str(bytearray(r['BodyPreview']))
        result = re.sub("bytearray\(", "", result)
        result = re.sub("\\'\)", "", result)
        return re.sub("b\\'", "", result)

    def purge(self):
        operation = {
            'type': 'exec',
            'mbean': self.queue_bean,
            'operation': 'purge()',
        }
        self.jolokia_session.request(operation)
