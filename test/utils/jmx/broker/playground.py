__author__ = 'tdpreece'
import requests
import json

from jolokia_session import JolokiaSession


session = JolokiaSession.connect('localhost', '28161')
get_queue_size_payload = {
    "type": "read",
    "mbean": "org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
    "attribute": "QueueSize"
}
session.request(get_queue_size_payload)


def get_queue_size():
    session = JolokiaSession.connect('localhost', '28161')
    get_queue_size_payload = {
        "type": "read",
        "mbean": "org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
        "attribute": "QueueSize"
    }
    queue_size = session.request(get_queue_size_payload)
    print "Queue size = {}".format(queue_size)

url  = 'http://localhost:28161/api/jolokia'
create_queue_payload = {
    "type":"exec",
    "mbean":"org.apache.activemq:type=Broker,brokerName=TEST.BROKER",
    "operation":"addQueue",
    "arguments":["test.req"]
}
r = requests.post(url, json=create_queue_payload)
print r

send_text_message_payload = {
    "type":"exec",
    "mbean":"org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
    "operation":"sendTextMessage(java.lang.String)",
    "arguments":["test message"]
}

r = requests.post(url, json=send_text_message_payload)
print "status code is 200 is {}".format(r.status_code == 200)
print r

print get_queue_size()

browse_messages_payload = {
    "type":"exec",
    "mbean":"org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
    "operation":"browse()"
}
r = requests.post(url, json=browse_messages_payload)
print r.text

purge_queue_payload = {
    "type":"exec",
    "mbean":"org.apache.activemq:type=Broker,brokerName=TEST.BROKER,destinationType=Queue,destinationName=test.req",
    "operation":"purge()"
}
r = requests.post(url, json=purge_queue_payload)
print r.text

print get_queue_size()