__author__ = 'tdpreece'
import stomp
import time
import json

from collections import OrderedDict


class Client(object):
    def __init__(self, hostname, port, username):
        pass

    def go_live_with(self):
        hosts = [('localhost', 21613)]
        conn = stomp.Connection(host_and_ports=hosts)
        conn.start()
        conn.connect(wait=True)
        conn.set_listener('my_listener', MyListener(conn))
        conn.subscribe(destination='test.req', id=1)
        time.sleep(1)
        conn.disconnect()


class MyListener(stomp.ConnectionListener):

    def __init__(self, conn):
        self.conn = conn

    def on_message(self, headers, message):
        decoded_message = json.loads(message)
        method = decoded_message['method']
        params = decoded_message['params']
        id = decoded_message['id']

        print('method: '+method+', params: '+str(params)+', id: '+id)

        if method == 'sum':
            result = int(params[0]) + int(params[1])
        elif method == 'increment':
            result = int(params[0]) + 1

        response = OrderedDict([
            ('result', result),
            ('error', None),
            ('id', id),
        ])

        self.conn.send(
            body=json.dumps(response, separators=(',', ':')),
            destination='test.resp'
        )
