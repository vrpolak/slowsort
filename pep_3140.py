"""Module providing few iterable types with str() respecting PEP 3140.

FIXME: Guard against possible cycles in graphs of references.
"""

from collections import deque


class List(list):
    """A list with str support."""

    def __str__(self):
        """Return comma+space separated str of items in square brackets."""
        return "[" + ", ".join([str(item) for item in self]) + "]"


class Tuple(tuple):
    """A tuple with str support."""

    def __str__(self):
        """Return comma+space separated str of items in round brackets."""
        return "(" + ", ".join([str(item) for item in self]) + ")"


class Dict(dict):
    """A dict with str support."""

    def __str__(self):
        """Return comma+space separated str of items in curly brackets."""
        return "{" + ", ".join([str(key) + ": " + str(value) for key, value in self.items()]) + "}"


class Deque(deque):
    """A deque with str support."""

    def __str__(self):
        """Return str of List corresponding to self."""
        # TODO: What about "Deque([1, 2, ...])"?
        return str(List(self))
