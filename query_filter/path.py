from query_filter import predicates


class Path:
    def __init__(self, *keys):
        self._keys = keys

    def __eq__(self, other):
        return predicates.Equals(self._keys, other)

