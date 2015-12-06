__author__ = 'tdpreece'
__author__ = 'tdpreece'
import logging
import sys
import stomp
import time
import json

from collections import OrderedDict


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
            conn.connect(wait=True)
            listener = MyListener(conn, implementation_map)
            conn.set_listener('listener', listener)
            conn.subscribe(destination='test.req', id=1, ack='client-individual')
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
        conn.set_listener('listener', listener)
        conn.subscribe(destination='test.req', id=1, ack='client-individual')
        time.sleep(1)
        conn.disconnect()


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn, implementation_map):
        self.conn = conn
        self.implementation_map = implementation_map

    def on_message(self, headers, message):
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
        print('id = {id}, req = {method}({params}), resp = {result}'.format(id=id, method=method, params=params_str, result=result))
        if result is not None:
            remote_broker = RemoteBroker(self.conn)
            remote_broker.acknowledge(headers)
            response = OrderedDict([
                ('result', result),
                ('error', None),
                ('id', id),
            ])
            remote_broker.publish(response)

class PeekListener(stomp.ConnectionListener):
    def __init__(self, conn, implementation_map):
        self.conn = conn
        self.implementation_map = implementation_map

    def on_message(self, headers, message):
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
        print('id = {id}, req = {method}({params}), resp = {result}'.format(id=id, method=method, params=params_str, result=result))


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