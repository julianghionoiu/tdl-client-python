class NoisyImplementationRunner:

    def __init__(self, deploy_message, audit_stream):
        self._deploy_message = deploy_message
        self._audit_stream = audit_stream

    def run(self):
        self._audit_stream.log(self._deploy_message)
