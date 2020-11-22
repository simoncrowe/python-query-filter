
class Path:
    def __init__(self, *keys):
        self._keys = keys

    def __eq__(self, other):
        return Equals(self._keys, other)

