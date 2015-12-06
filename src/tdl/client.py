__author__ = 'tdpreece'
__author__ = 'tdpreece'
import logging
import time
import json
from collections import OrderedDict

import stomp

logger = logging.getLogger('tdl.client')
logger.addHandler(logging.NullHandler())


class Client(object):
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port

    def go_live_with(self, implementation_map):
        hosts = [(self.hostname, self.port)]
        try:
            conn = stomp.Connection(host_and_ports=hosts)
            conn.start()
            handling_strategy = RespondToAllRequests()
            listener = Listener(conn, implementation_map, handling_strategy)
            conn.connect(wait=True)
            remote_broker = RemoteBroker(conn)
            remote_broker.subscribe(listener)
            time.sleep(1)
            conn.disconnect()
        except Exception as e:
            logger.exception('Problem communicating with the broker.')

    def trial_run_with(self, implementation_map):
        hosts = [(self.hostname, self.port)]
        conn = stomp.Connection(host_and_ports=hosts)
        conn.start()
        conn.connect(wait=True)
        handling_strategy = PeekAtFirstRequest()
        listener = Listener(conn, implementation_map, handling_strategy)
        remote_broker = RemoteBroker(conn)
        remote_broker.subscribe(listener)
        time.sleep(1)
        conn.disconnect()

class RespondToAllRequests(object):
    @staticmethod
    def process_next_message_from(implementation_map, remote_broker, headers, message):
        response = Listener.respond_to(implementation_map, message)
        if response is not None:
            remote_broker.acknowledge(headers)
            remote_broker.publish(response)

class PeekAtFirstRequest(object):
    @staticmethod
    def process_next_message_from(implementation_map, remote_broker, headers, message):
        Listener.respond_to(implementation_map, message)

class Listener(stomp.ConnectionListener):
    def __init__(self, conn, implementation_map, handling_strategy):
        self.conn = conn
        self.remote_broker = RemoteBroker(self.conn)
        self.implementation_map = implementation_map
        self.handling_strategy = handling_strategy

    def on_message(self, headers, message):
        self.handling_strategy.process_next_message_from(self.implementation_map, self.remote_broker, headers, message)

    @staticmethod
    def respond_to(implementation_map, message):
        decoded_message = json.loads(message)
        method = decoded_message['method']
        params = decoded_message['params']
        id = decoded_message['id']
        implementation = implementation_map[method]
        try:
           result = implementation(params)
        except Exception as e:
           logger.info('The user implementation has thrown an exception: {}'.format(e.message))
           result = None
        params_str = ", ".join([str(p) for p in params])
        print('id = {id}, req = {method}({params}), resp = {result}'.format(id=id, method=method, params=params_str,
                                                                           result=result))
        if result is not None:
            response = OrderedDict([
                ('result', result),
                ('error', None),
                ('id', id),
                ])
        return response


class RemoteBroker(object):
    def __init__(self, conn):
        self.conn = conn

    def acknowledge(self, headers):
        self.conn.ack(headers['message-id'], headers['subscription'])

    def publish(self, response):
        self.conn.send(
            body=json.dumps(response, separators=(',', ':')),
            destination='test.resp'
        )

    def subscribe(self, listener):
        self.conn.set_listener('listener', listener)
        self.conn.subscribe(destination='test.req', id=1, ack='client-individual')
