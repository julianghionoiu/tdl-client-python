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
            listener = MyListener(conn, implementation_map)
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
        listener = PeekListener(conn, implementation_map)
        remote_broker = RemoteBroker(conn)
        remote_broker.subscribe(listener)
        time.sleep(1)
        conn.disconnect()


class Listener(stomp.ConnectionListener):
    def __init__(self, conn, implementation_map):
        self.conn = conn
        self.remote_broker = RemoteBroker(self.conn)
        self.implementation_map = implementation_map

    def on_message(self, headers, message):
        self.process_next_message_from(headers, message)

    def respond_to(self, message):
        decoded_message = json.loads(message)
        method = decoded_message['method']
        params = decoded_message['params']
        id = decoded_message['id']
        implementation = self.implementation_map[method]
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


class MyListener(Listener):
    def process_next_message_from(self, headers, message):
        response = self.respond_to(message)
        if response is not None:
            self.remote_broker.acknowledge(headers)
            self.remote_broker.publish(response)


class PeekListener(Listener):
    def process_next_message_from(self, headers, message):
        self.respond_to(message)


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
