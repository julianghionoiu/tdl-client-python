from tdl.queue.processing_rules import ProcessingRules
from tdl.queue.actions.publish_action import PublishAction
from tdl.queue.transport.remote_broker import RemoteBroker


class QueueBasedImplementationRunner:

    def __init__(self, config, deploy_processing_rules):
        self._config = config
        self._deploy_processing_rules = deploy_processing_rules
        self._audit = QueueBasedImplementationRunnerAudit(config.get_audit_stream())

    def run(self):
        self._audit.log_line('Starting client')

        try:
            remote_broker = RemoteBroker(
                self._config.get_hostname(),
                self._config.get_port(),
                self._config.get_unique_id(),
                self._config.get_request_timeout_millis())
            remote_broker.subscribe(ApplyProcessingRules(self._deploy_processing_rules, self._audit))

            self._audit.log_line('Stopping client')
        except Exception as e:
            self._audit.log_exception('There was a problem processing messages', e)

        self._audit.log_line('Stopping client')


class QueueBasedImplementationRunnerAudit:

    def __init__(self, audit_stream):
        self._audit_stream = audit_stream
        self._lines = []

        self.start_line()

    def start_line(self):
        self._lines.clear()

    def log(self, auditable):
        text = auditable.get_audit_text()
        self._lines.append(text)

    def end_line(self):
        text = '\n'.join(self._lines)
        self._audit_stream.print(text)

    def log_exception(self, message, e):
        self.start_line()
        self._lines.append('{0}: {1}'.format(message, str(e)))
        self.end_line()

    def log_line(self, text):
        self.start_line()
        self._lines.append(text)
        self.end_line()


class QueueBasedImplementationRunnerBuilder:

    def __init__(self):
        self._deploy_processing_rules = ProcessingRules()
        self._config = None

        self._deploy_processing_rules.\
            on('display_description').\
            call(lambda _: 'OK').\
            then(PublishAction)

    def set_config(self, config):
        self._config = config
        return self

    def with_solution_for(self, method_name, user_implementation, action):
        self._deploy_processing_rules.\
            on(method_name).\
            call(user_implementation).\
            then(action)

    def create(self):
        return QueueBasedImplementationRunner(self._config, self._deploy_processing_rules)


class ApplyProcessingRules:

    def __init__(self, processing_rules, audit):
        self._processing_rules = processing_rules
        self._audit = audit

    def process_next_request_from(self, remote_broker, request):
        self._audit.start_line()
        self._audit.log(request)

        response = self._processing_rules.get_response_for(request)
        self._audit.log(response)

        client_action = response.client_action
        self._audit.log(client_action)

        self._audit.end_line()

        client_action.after_response(remote_broker, request, response)

        return client_action.prepare_for_next_request(remote_broker)
