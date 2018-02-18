class ProcessingRule:

    def __init__(self, user_implementation, client_action):
        self._user_implementation = user_implementation
        self._client_action = client_action

    def get_user_implementation(self):
        return self._user_implementation

    def get_client_action(self):
        return self._client_action
