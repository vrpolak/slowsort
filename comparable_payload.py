"""Module that defines ComparablePayload class, useful for overriding comparisons."""

from functools import total_ordering


@total_ordering
class ComparablePayload(object):
    """Pair of key and payload, comparable by key. Can be used to store sorted pairs."""

    def __init__(self, key, payload):
        """Wrap key and payload into single object."""
        self.key = key
        self.payload = payload

    def __eq__(self, other):
        """Equality test, delegating to key equality."""
        return self.key == other.key

    def __lt__(self, other):
        """Less-than test, delegating to key comparison."""
        return self.key < other.key

    def __str__(self):
        """Return class name and key string in parentheses."""
        return "ComparablePayload(" + str(self.key) + ")"

    def __repr__(self):
        """Return constructor-like string."""
        return "ComparablePayload(" + repr(self.key) + ", " + repr(self.payload) + ")"
