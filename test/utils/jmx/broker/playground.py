__author__ = 'tdpreece'
import requests
import json

from jolokia_session import JolokiaSession
from remote_jmx_queue import RemoteJmxQueue
from remote_jmx_broker import RemoteJmxBroker

session = JolokiaSession.connect('localhost', '28161')
get_queue_size_payload = {
    "type": "read",
    "mbean": "org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
    "attribute": "QueueSize"
}
session.request(get_queue_size_payload)


url  = 'http://localhost:28161/api/jolokia'
create_queue_payload = {
    "type":"exec",
    "mbean":"org.apache.activemq:type=Broker,brokerName=TEST.BROKER",
    "operation":"addQueue",
    "arguments":["test.req"]
}
r = session.request(create_queue_payload)
print r

queue = RemoteJmxQueue(session, broker_name='TEST.BROKER', queue_name='test.req')
queue.send_text_message("Message from RemoteJmxQueue")

print "Queue size = {}".format(queue.get_size())
print "Message contents = {}".format(queue.get_message_contents())

queue.purge()

print "Queue size = {}".format(queue.get_size())


# ******** Using Broker **********

broker = RemoteJmxBroker.connect('localhost', '28161','TEST.BROKER')
broker.add_queue('test_queue')