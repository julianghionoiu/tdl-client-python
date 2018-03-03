import sys
import time

from behave import given, step, then, use_step_matcher, when
from hamcrest import assert_that, contains_string, equal_to, is_
from cStringIO import StringIO
from tdl.queue.implementation_runner_config import ImplementationRunnerConfig
from tdl.queue.queue_based_implementation_runner import QueueBasedImplementationRunnerBuilder
from tdl.queue.actions.client_actions import ClientActions

use_step_matcher("re")


HOSTNAME = 'localhost'
STOMP_PORT = 21613


@given('I start with a clean broker and a client for user \"([^"]*)\"')
def create_the_queues(context, unique_id):
    context.request_queue = context.broker.add_queue('{}.req'.format(unique_id))
    context.request_queue.purge()

    context.response_queue = context.broker.add_queue('{}.resp'.format(unique_id))
    context.response_queue.purge()

    config = ImplementationRunnerConfig()\
        .set_hostname(HOSTNAME)\
        .set_port(STOMP_PORT)\
        .set_unique_id(unique_id)

    context.queue_implementation_runner_builder = QueueBasedImplementationRunnerBuilder()\
        .set_config(config)
    context.queue_implementation_runner = context.queue_implementation_runner_builder.create()


@given("the broker is not available")
def client_with_wrong_broker(context):
    config = ImplementationRunnerConfig()\
        .set_hostname('111')\
        .set_port(STOMP_PORT)\
        .set_unique_id('X')

    context.queue_implementation_runner_builder = QueueBasedImplementationRunnerBuilder()\
        .set_config(config)


@then("the time to wait for requests is (\d+)ms")
def check_time(context, expected_timeout):
    assert_that(
        context.queue_implementation_runner.get_request_timeout_millis(),
        is_(equal_to(int(expected_timeout))),
        "The client request timeout has a different value.")


@then('the request queue is \"([^"]*)\"')
def check_request_queue(context, expected_value):
    assert_that(
        context.request_queue.get_name(),
        is_(equal_to(expected_value)),
        "Request queue has a different value.")


@then('the response queue is \"([^"]*)\"')
def check_response_queue(context, expected_value):
    assert_that(
        context.response_queue.get_name(),
        is_(equal_to(expected_value)),
        "Request queue has a different value."
    )


@given("I receive the following requests")
def initialize_request_queue(context):
    for row in context.table:
        payload = row[0]
        context.request_queue.send_text_message(payload)

    context.request_count = context.request_queue.get_size()


@given("I receive (\d+) identical requests like")
def receive_multiple_identical_request(context, num):
    for x in xrange(int(num)):
        for row in context.table:
            payload = row[0]
            context.request_queue.send_text_message(payload)

    context.request_count = context.request_queue.get_size()


# ~~~~~ Implementations


def do_slow_work(t):
    time.sleep(t/1000.00)
    return "OK"


def get_implementation(implementation_name):
    test_implementations = {
        'add two numbers': lambda x, y: x + y,
        'increment number': lambda x: x + 1,
        'return null': lambda *args: None,
        'throw exception': lambda param: raise_(Exception('faulty user code')),
        'some logic': lambda: "ok",
        'echo the request': lambda req: req,
        'work for 600ms': lambda param: do_slow_work(600),
    }

    if implementation_name in test_implementations:
        return test_implementations[implementation_name]
    else:
        raise KeyError('Not a valid implementation reference: "' + implementation_name + "\"")


CLIENT_ACTIONS = {
    'publish': ClientActions.publish(),
    'stop': ClientActions.stop()
}


@when("I go live with the following processing rules")
def step_impl(context):
    for row in context.table:
        context.queue_implementation_runner_builder\
            .with_solution_for(
                row[0],
                get_implementation(row[1]),
                CLIENT_ACTIONS[row[2]])

    context.queue_implementation_runner = context.queue_implementation_runner_builder.create()

    # with Capturing() as context.stdout_capture:
    context.queue_implementation_runner.run()


# ~~~~~ Assertions


@then("the client should consume all requests")
def request_queue_empty(context):
    assert_that(context.request_queue.get_size(), is_(equal_to(0)), "Requests have not been consumed")


@step("the client should publish the following responses")
def response_queue_contains_expected(context):
    expected_responses = [row[0] for row in context.table]
    assert_that(context.response_queue.get_message_contents(), is_(equal_to(expected_responses)),
                "The responses are not correct")


@then("the client should display to console")
def the_client_should_display_to_console(context):
    for row in context.table:
        assert_that(
            context.stdout_capture.getvalue(),
            contains_string(row[0])
        )


@step("the client should not display to console")
def the_client_should_not_display_to_console(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])


@then("the client should not consume any request")
def request_queue_unchanged(context):
    assert_that(
        context.request_queue.get_size(),
        is_(equal_to(context.request_count)),
        "Requests have been consumed"
    )


@then(u'the client should consume first request')
def step_impl(context):
    assert_that(
        context.request_queue.get_size(),
        is_(equal_to(context.request_count - 1)),
        "Wrong number of requests have been consumed."
    )


@step("the client should not publish any response")
def response_queue_unchanged(context):
    assert_that(
        context.response_queue.get_size(),
        is_(equal_to(0)),
        "The response queue has different size. Messages have been published"
    )


@then("I should get no exception")
def i_should_get_no_exception(_):
    # OBS if you get here there were no exceptions
    pass


@then('the processing time should be lower than (\d+)ms')
def processing_time_should_be_lower_than(context, num):
    print("total_processing_time " + str(context.queue_implementation_runner.total_processing_time_millis))
    assert(num > context.queue_implementation_runner.total_processing_time_millis)


# ~~~~ Helpers

def raise_(ex):
    raise ex


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        sys.stdout = self._stdout

    def getvalue(self):
        return self._stringio.getvalue()
