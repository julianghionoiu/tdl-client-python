from tdl.queue.actions.publish_action import PublishAction
from tdl.queue.actions.publish_and_stop_action import PublishAndStopAction
from tdl.queue.actions.stop_action import StopAction


class ClientActions:

    def __init__(self):
        pass

    @staticmethod
    def publish():
        return PublishAction

    @staticmethod
    def stop():
        return StopAction

    @staticmethod
    def publish_and_stop():
        return PublishAndStopAction
