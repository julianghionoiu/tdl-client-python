from behave import given, step, then, use_step_matcher, when
from tdl.client import Client


use_step_matcher("re")

# ~~~~~ Setup


@given("I start with a clean broker")
def create_the_queues(context):
    request_queue = context.broker.add_queue('test.req')
    request_queue.purge()
    response_queue = context.broker.add_queue('test.resp')
    response_queue.purge()
    hostname = 'localhost'
    stomp_port = '21613'
    username = 'test'
    context.client = Client(hostname, stomp_port, username)


@given("the broker is not available")
def client_with_wrong_broker(context):
    pass


@given("I receive the following requests")
def initialize_request_queue(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])

    pass


# ~~~~~ Implementations

@when("I go live with the following implementations")
def step_impl(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])

    pass

@when("I do a trial run with the following implementations")
def step_impl(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])

    pass

# ~~~~~ Assertions


@then("the client should consume all requests")
def request_queue_empty(context):
    pass


@step("the client should publish the following responses")
def response_queue_contains_expected(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])
    pass


@then("the client should display to console")
def the_client_should_display_to_console(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])
    pass


@step("the client should not display to console")
def the_client_should_not_display_to_console(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])
    pass


@then("the client should not consume any request")
def request_queue_unchanged(context):
    pass


@step("the client should not publish any response")
def response_queue_unchanged(context):
    pass


@then("I should get no exception")
def i_should_get_no_exception(context):
    pass


