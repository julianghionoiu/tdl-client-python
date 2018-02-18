class StopAction:

    @staticmethod
    def get_audit_text():
        return '(NOT PUBLISHED'

    @staticmethod
    def after_response():
        # Do nothing.
        pass

    @staticmethod
    def prepare_for_next_request(remote_broker):
        remote_broker.close()  # TODO
