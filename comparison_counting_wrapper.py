"""Module that defines a wrapper object which counts comparisons.

This uses functools to generate rich comparison functions.
Equivalence test does not increment counter, as sorts never do
equal test directly, and with that every comparison increments counter exactly once.

In order to support queues that require hashable items,
hash function is implemented, and the has value
does not change with the comparison counter.
"""

from functools import total_ordering


# TODO: Make sure copy.deepcopy() is supported.
class SimpleCounter(object):
    """A simple counter to use."""

    def __init__(self):
        """Initialization."""
        self.count = 0


@total_ordering
class ComparisonCountingWrapper(object):
    """A wrapper for values which counts comparison operations."""

    def __init__(self, value, counter):
        """Wrap the value using the counter object."""
        self.value = value
        self.counter = counter

    def __hash__(self):
        """Return hash of the wrapped value."""
        return hash(self.value)

    def __eq__(self, other):
        """Equality test, NOT incrementing counter."""
        return self.value == other.value

    def __lt__(self, other):
        """Less-than test, incrementing counter."""
        self.counter.count += 1
        return self.value < other.value

    def __str__(self):
        """Return class name followed by string value in parentheses."""
        return "ComparisonCountingWrapper(" + str(self.value) + ")"

    def __repr__(self):
        """Return constructor-like string."""
        return "ComparisonCountingWrapper(" + repr(self.value) + ", " + repr(self.counter) + ")"
