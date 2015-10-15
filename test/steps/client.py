from behave import *

use_step_matcher("re")

# ~~~~~ Setup

@given("I start with a clean broker")
def create_the_queues(context):
    pass


@given("the broker is not available")
def client_with_wrong_broker(context):
    pass


@given("I receive the following requests")
def initialize_request_queue(context):
    for row in context.table:
        print(row)

    pass


# ~~~~~ Implementations

@when("I go live with an implementation that adds two numbers")
def step_impl(context):
    pass


@then("the client should consume all requests")
def step_impl(context):
    pass


@step("the client should publish the following responses")
def step_impl(context):
    pass


@then("the client should display to console")
def step_impl(context):
    pass


@when("I go live with an implementation that returns null")
def step_impl(context):
    pass


@then("the client should not consume any request")
def step_impl(context):
    pass


@step("the client should not publish any response")
def step_impl(context):
    pass


@when("I go live with an implementation that throws exception")
def step_impl(context):
    pass


@when("I go live with an implementation that is valid")
def step_impl(context):
    pass


@then("I should get no exception")
def step_impl(context):
    pass


@when("I do a trial run with an implementation that adds two numbers")
def step_impl(context):
    pass


@step("the client should not display to console")
def step_impl(context):
    pass