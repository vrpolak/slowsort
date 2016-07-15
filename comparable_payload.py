"""Module that defines ComparablePayload class, useful for overriding comparisons."""


class ComparablePayload(object):
    """Pair of key and payload, comparable by key. Can be used to store sorted pairs."""

    def __init__(self, key, payload):
        self.key = key
        self.payload = payload

    def __cmp__(self, other):
        return self.key.__cmp__(other.key)

    def __str__(self):
        return "ComparablePayload(" + str(self.key) + ")"

    def __repr__(self):
        return "ComparablePayload(" + repr(self.key) + ", " + repr(self.payload) + ")"
