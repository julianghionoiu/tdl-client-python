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
        pass

    def go_live_with(self, implementation_map):
        hosts = [('localhost', 21613)]
        conn = stomp.Connection(host_and_ports=hosts)
        conn.start()
        conn.connect(wait=True)
        conn.set_listener('my_listener', MyListener(conn, implementation_map))
        conn.subscribe(destination='test.req', id=1, ack='client-individual')
        time.sleep(1)
        conn.disconnect()

    def trial_run_with(self, implementation_map):
        hosts = [('localhost', 21613)]
        conn = stomp.Connection(host_and_ports=hosts)
        conn.start()
        conn.connect(wait=True)
        conn.set_listener('peek_listener', PeekListener(conn, implementation_map))
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
            self.conn.ack(headers['message-id'], headers['subscription'])
            response = OrderedDict([
                ('result', result),
                ('error', None),
                ('id', id),
            ])
            self.conn.send(
                body=json.dumps(response, separators=(',', ':')),
                destination='test.resp'
            )

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
