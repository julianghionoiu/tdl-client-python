__author__ = 'tdpreece'

from jolokia_session import JolokiaSession
from remote_jmx_queue import RemoteJmxQueue
from remote_jmx_broker import RemoteJmxBroker

broker = RemoteJmxBroker.connect('localhost', '28161','TEST.BROKER')
queue = broker.add_queue('test_queue')

queue.send_text_message("Message from RemoteJmxQueue")
print "Queue size = {}".format(queue.get_size())
print "Message contents = {}".format(queue.get_message_contents())

queue.send_text_message("Another Message from RemoteJmxQueue")
print "Queue size = {}".format(queue.get_size())
print "Message contents = {}".format(queue.get_message_contents())


queue.purge()

print "Queue size = {}".format(queue.get_size())
