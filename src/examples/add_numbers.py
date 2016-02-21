import logging
import sys

from tdl.client import Client
from tdl.processing_rules import ProcessingRules

def setup_logging():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    logger = logging.getLogger('tdl.client')
    logger.setLevel(logging.INFO)
    logger.addHandler(ch)


setup_logging()


def run_client():
    client = Client(hostname='localhost', username='julian')

    rules = ProcessingRules()
    rules.on("display_description").call(lambda label, description: "OK").then("publish")
    rules.on("sum").call(add_numbers).then("publish")
    rules.on("end_round").call(lambda params: "OK").then("publish_and_stop")

    client.go_live_with(rules)


# def add_numbers(params):
#     return params[0] + params[1]

def add_numbers(x, y):
    return x + y


run_client()
