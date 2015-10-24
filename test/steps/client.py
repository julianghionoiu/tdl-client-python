from behave import *


use_step_matcher("re")

# ~~~~~ Setup


@given("I start with a clean broker")
def create_the_queues(context):
    request_queue = context.broker.add_queue('test.req')
    request_queue.purge()
    response_queue = context.broker.add_queue('test.resp')
    response_queue.purge()


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

@when("I go live with an implementation that (?P<does_something>.*)")
def go_live(context, does_something):
    print(does_something)
    pass


@when("I do a trial run with an implementation that (?P<does_something>.*)")
def trial_run(context, does_something):
    print(does_something)
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
