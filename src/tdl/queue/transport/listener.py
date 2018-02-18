from stomp import ConnectionListener


class Listener(ConnectionListener):
    def __init__(self, remote_broker, handling_strategy, start_timer, stop_timer):
        self._remote_broker = remote_broker
        self._handling_strategy = handling_strategy
        self._start_timer = start_timer
        self._stop_timer = stop_timer

    def on_message(self, headers, message):
        self._stop_timer()
        self._handling_strategy.process_next_message_from(self._remote_broker, headers, message)
        self._start_timer()
