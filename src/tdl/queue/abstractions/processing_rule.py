class ProcessingRule:

    def __init__(self, user_implementation, client_action):
        self.user_implementation = user_implementation
        self.client_action = client_action

    def get_user_implementation(self):
        return self.user_implementation

    def get_client_action(self):
        return self.client_action
