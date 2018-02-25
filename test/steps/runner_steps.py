from behave import given, then, use_step_matcher, when
from hamcrest import assert_that, contains_string, is_
import shutil

from test.runner.test_audit_stream import TestAuditStream
from test.runner.noisy_implementation_runner import NoisyImplementationRunner
from test.runner.quiet_implementation_runner import QuietImplementationRunner
from test.runner.wiremock_process import WiremockProcess
from tdl.runner.challenge_session_config import ChallengeSessionConfig
from tdl.runner.challenge_session import ChallengeSession


use_step_matcher("re")


audit_stream = TestAuditStream()
implementation_runner = QuietImplementationRunner()


@given('^There is a challenge server running on "([^"]*)" port ([^"]*)$')
def setup_challenge_server(context, hostname, port):
    context.challenge_hostname = hostname
    context.challenge_port = port

    context.challenge_server_stub = WiremockProcess(hostname, port)
    context.challenge_server_stub.reset()


@given('^There is a recording server running on "([^"]*)" port ([^"]*)$')
def setup_recording_server(context, hostname, port):
    context.recording_server_stub = WiremockProcess(hostname, port)
    context.recording_server_stub.reset()


@given('^journeyId is "([^"]*)"$')
def journey_is(context, journey_id):
    context.journey_id = journey_id


@given('^the challenge server exposes the following endpoints$')
def configure_challenge_server_endpoints(context):
    for config in context.table:
        context.challenge_server_stub.create_new_mapping(config)


@given('^the recording server exposes the following endpoints$')
def configure_recording_server_endpoints(context):
    for config in context.table:
        context.recording_server_stub.create_new_mapping(config)


@given('^the action input comes from a provider returning "(.*)"$')
def action_input_comes_from_a_provider_returning(context, s):
    context.action_provider_callback = lambda: s


@given('^the challenges folder is empty$')
def challenges_folder_is_empty():
    shutil.rmtree('challenges', ignore_errors=True)


@given('^there is an implementation runner that prints "(.*)"$')
def there_is_an_implementation_runner_that_prints(context, s):
    context.implementation_runner_message = s
    context.implementation_runner = NoisyImplementationRunner(s, audit_stream)


@given('^recording server is returning error$')
def recording_server_is_returning_error(context):
    context.recording_server_stub.reset()


@given('^the challenge server returns (.*), response body "(.*)" for all requests$')
def challenge_server_returns_response_body_for_all_requests(context, return_code, body):
    context.challenge_server_stub.create_new_mapping({
        'endpointMatches': '^(.*)',
        'status': return_code,
        'verb': 'ANY',
        'responseBody': body
    })


@given('^the challenge server returns (.*) for all requests$')
def challenge_server_returns_for_all_requests(context, return_code):
    context.challenge_server_stub.create_new_mapping({
        'endpointMatches': '^(.*)',
        'status': return_code,
        'verb': 'ANY'
    })


@when('^user starts client$')
def user_starts_client(context):
    config = ChallengeSessionConfig.for_journey(context.journey_id)\
        .with_server_hostname(context.challenge_hostname)\
        .with_port(context.challenge_port)\
        .with_colours(True)\
        .with_audit_stream(audit_stream)\
        .with_recording_system_should_be_on(True)

    ChallengeSession.for_runner(implementation_runner)\
        .with_config(config)\
        .with_action_provider(context.action_provider_callback)\
        .start()


@then('^the server interaction should look like:$')
def server_interaction_should_look_like(_, expected_output):
    total = audit_stream.get_log()
    assert_that(total, is_(expected_output), 'Expected string is not contained in output')


@then('^the file "(.*)" should contain$')
def the_file_should_contain(_, file_, text):
    with open(file_, 'r') as f:
        content = f.read()
    assert_that(content, is_(text), 'Contents of the file is not what is expected')


@then('^the recording system should be notified with "(.*)"$')
def the_recording_system_should_be_notified_with(context, expected_output):
    endpoint_was_hit = context.recording_server_stub.verify_endpoint_was_hit('/notify', 'POST', expected_output)
    assert_that(endpoint_was_hit, is_(True))


@then('^the implementation runner should be run with the provided implementations$')
def the_implementation_runner_should_be_run_with_provided_implementations(context):
    total = audit_stream.get_log()
    assert_that(total, not contains_string(context.implementation_runner_message))


@then('^the server interaction should contain the following lines:$')
def the_server_interaction_should_contain_the_following_lines(_, expected_output):
    total = audit_stream.get_log()
    lines = expected_output.split('\n')
    for line in lines:
        assert_that(total, not contains_string(line), 'Expected string is not contained in output')


@then('^the client should not ask the user for input$')
def the_client_should_not_ask_the_user_for_input():
    total = audit_stream.get_log()
    assert_that(total, not contains_string('Selected action is:'))
