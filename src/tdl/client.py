__author__ = 'tdpreece'
import stomp
import time
import json

from collections import OrderedDict


class Client(object):
    def __init__(self, hostname, port, username):
        pass

    def go_live_with(self, implementation_map):
        hosts = [('localhost', 21613)]
        conn = stomp.Connection(host_and_ports=hosts)
        conn.start()
        conn.connect(wait=True)
        conn.set_listener('my_listener', MyListener(conn, implementation_map))
        conn.subscribe(destination='test.req', id=1)
        time.sleep(1)
        conn.disconnect()

    def trial_run_with(self, implementation_map):
        self.go_live_with(implementation_map)


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
        result = implementation(params)

        response = OrderedDict([
            ('result', result),
            ('error', None),
            ('id', id),
        ])

        self.conn.send(
            body=json.dumps(response, separators=(',', ':')),
            destination='test.resp'
        )
