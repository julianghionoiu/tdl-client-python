import sys

from behave import given, step, then, use_step_matcher, when
from hamcrest import assert_that, contains_string, equal_to, is_
from cStringIO import StringIO
from tdl.client import Client
from tdl.processing_rules import ProcessingRules

use_step_matcher("re")


# ~~~~~ Setup


@given("I start with a clean broker")
def create_the_queues(context):
    username = 'test'
    context.request_queue = context.broker.add_queue('{}.req'.format(username))
    context.request_queue.purge()
    context.response_queue = context.broker.add_queue('{}.resp'.format(username))
    context.response_queue.purge()
    hostname = 'localhost'
    stomp_port = 21613
    context.client = Client(hostname=hostname, username=username, port=stomp_port)


@given("the broker is not available")
def client_with_wrong_broker(context):
    incorrect_hostname = 'localhost'
    stomp_port = 11613
    username = 'test'
    context.client = Client(hostname=incorrect_hostname, username=username, port=stomp_port)


@given("I receive the following requests")
def initialize_request_queue(context):
    requests = table_as_list(context)
    for request in requests:
        context.request_queue.send_text_message(request)
    context.request_count = context.request_queue.get_size()


# ~~~~~ Implementations


def get_implementation(implementation_name):
    test_implementations = {
        'add two numbers': lambda x, y: x + y,
        'increment number': lambda x: x + 1,
        'return null': lambda *args: None,
        'throw exception': lambda param: raise_(Exception('faulty user code')),
        'some logic': lambda param: "ok",
        'echo the request': lambda req: req,
    }

    if implementation_name in test_implementations:
        return test_implementations[implementation_name]
    else:
        raise KeyError('Not a valid implementation reference: "' + implementation_name + "\"")


@when("I go live with the following processing rules")
def step_impl(context):
    processing_rules = ProcessingRules()
    for row in table_as_list_of_rows(context):
        method = row[0]
        user_implementation = get_implementation(row[1])
        action = row[2]
        processing_rules.on(method).call(user_implementation).then(action)

    with Capturing() as context.stdout_capture:
        context.client.go_live_with(processing_rules)

# ~~~~~ Assertions

@then("the client should consume all requests")
def request_queue_empty(context):
    assert_that(context.request_queue.get_size(), is_(equal_to(0)), "Requests have not been consumed")


@step("the client should publish the following responses")
def response_queue_contains_expected(context):
    expected_responses = table_as_list(context)
    assert_that(context.response_queue.get_message_contents(), is_(equal_to(expected_responses)),
                "The responses are not correct")


@then("the client should display to console")
def the_client_should_display_to_console(context):
    assert_that(
        context.stdout_capture.getvalue(),
        contains_string(context.table.headings[0])
    ) 
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
def i_should_get_no_exception(context):
    # OBS if you get here there were no exceptions
    pass


# ~~~~ Helpers
def table_as_list_of_rows(context):
    return [row for row in context.table]


def table_as_list(context):
    return [context.table.headings[0]] + [row[0] for row in context.table]


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
