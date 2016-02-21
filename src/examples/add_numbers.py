import logging
import sys

from tdl.client import Client
from tdl.processing_rules import ProcessingRules

# Configure logging
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
logger = logging.getLogger('tdl.client')
logger.setLevel(logging.INFO)
logger.addHandler(ch)


def display_description(params):
    return display_round_id_and_info(params[0], params[1])


def display_round_id_and_info(round_id, info):
    print('Starting round: '.format(round_id))
    print(info)
    return 'OK'


class App:
    def main(self):
        implementation_map = {
            'display_description': {
                'test_implementation': display_description,
                'action': 'publish'
            },
            'increment': {
                'test_implementation': lambda x: x[0] + 1,
                'action': 'publish'
            },
            'sum': {
                'test_implementation': sum,
                'action': 'stop'
            },
        }

        processing_rules = ProcessingRules()

        client = Client(hostname='localhost', username='julian')
        client.go_live_with(processing_rules)

    @staticmethod
    def sum(x, y):
        return x + y


# Run

a = App()
a.main()
