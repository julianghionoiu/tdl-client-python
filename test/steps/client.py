from behave import given, step, then, use_step_matcher, when
from hamcrest import assert_that, equal_to, is_
from tdl.client import Client


use_step_matcher("re")

# ~~~~~ Setup


@given("I start with a clean broker")
def create_the_queues(context):
    context.request_queue = context.broker.add_queue('test.req')
    context.request_queue.purge()
    context.response_queue = context.broker.add_queue('test.resp')
    context.response_queue.purge()
    hostname = 'localhost'
    stomp_port = '21613'
    username = 'test'
    context.client = Client(hostname, stomp_port, username)


@given("the broker is not available")
def client_with_wrong_broker(context):
    pass


@given("I receive the following requests")
def initialize_request_queue(context):
    requests = table_as_list(context)
    for request in requests:
        context.request_queue.send_text_message(request)


# ~~~~~ Implementations

TEST_IMPLEMENTATIONS = {
    'adds two numbers': lambda params: int(params[0]) + int(params[1]),
    'increment number': lambda params: int(params[0]) + 1,
    'returns null': lambda params: None
}

@when("I go live with the following implementations")
def step_impl(context):
    implementation_map = {}
    for row in table_as_list_of_rows(context):
        implementation_map[row[0]] = TEST_IMPLEMENTATIONS[row[1]]
    context.client.go_live_with(implementation_map)


@when("I do a trial run with the following implementations")
def step_impl(context):
    print(context.table.headings[0])
    for row in context.table:
        print(row[0])

    context.client.go_live_with()


# ~~~~~ Assertions


@then("the client should consume all requests")
def request_queue_empty(context):
    assert_that(context.request_queue.get_size(), is_(equal_to(0)), "Requests have not been consumed")

@step("the client should publish the following responses")
def response_queue_contains_expected(context):
    expected_responses = table_as_list(context)
    assert_that(context.response_queue.get_message_contents(),  is_(equal_to(expected_responses)), "The responses are not correct" )


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

# ~~~~ Helpers
def table_as_list_of_rows(context):
    return [context.table.headings] + [row for row in context.table]


def table_as_list(context):
    return [context.table.headings[0]] + [row[0] for row in context.table]
