__author__ = 'tdpreece'
import stomp
import time


class Client(object):
    def __init__(self, hostname, port, username):
        pass


    def go_live_with(self):
        hosts = [('localhost', 21613)]
        conn = stomp.Connection(host_and_ports=hosts)
        conn.start()
        conn.connect(wait=True)
        conn.subscribe(destination='test.req', id=1)
        time.sleep(1)
        conn.disconnect()
