from __future__ import print_function


class TestAuditStream:

    def __init__(self):
        self._total = ''

    def log(self, s):
        print(s)
        self._total += '{}\n'.format(s)

    def get_log(self):
        return self._total

    def clear_log(self):
        self._total = ''
