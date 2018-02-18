class PublishAction:

    @staticmethod
    def get_audit_text():
        return ''

    @staticmethod
    def after_response(remote_broker, request, response):
        remote_broker.respond_to(request, response)  # TODO

    @staticmethod
    def prepare_for_next_request(remote_broker):
        remote_broker.receive()  # TODO
