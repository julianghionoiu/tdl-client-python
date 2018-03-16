class LogAuditStream:

    def __init__(self):
        self._lines = []

    def log(self, value):
        self._lines.append(value)

    def clear_log(self):
        self._lines[:] = []

    def get_log(self):
        return '\n'.join(self._lines)
