import sys, os
test_dir = os.path.dirname(__file__)
src_dir = os.path.join(os.path.dirname(test_dir), 'src')
sys.path.append(src_dir)

from utils.jmx.broker.remote_jmx_broker import RemoteJmxBroker

def before_all(context):
    context.broker = RemoteJmxBroker.connect(
        'localhost',
        '28161',
        'localhost'
    )


def before_feature(context, _):
    context.action_provider_callback = lambda: None
