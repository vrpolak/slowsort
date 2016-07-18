"""Module that defines a wrapper object which logs comparisons.

This uses functools to generate rich comparison functions.
Equivalence test does not log as sorts never do equal test directly,
and with that every comparison logs exactly once."""


from functools import total_ordering


@total_ordering
class ComparisonLoggingWrapper(object):
    """A wrapper for values which logs comparison operations"""

    def __init__(self, value, log):
        """Wrap the value using the log object."""
        self.value = value
        self.log = log

    def __eq__(self, other):
        """Equality test, NOT logging."""
        return self.value == other.value

    def __lt__(self, other):
        """Less-than test, logging result."""
        self.log.info("Called less-than on wrapped value: %s", self.value)
        self.log.info("against wrapped value: %s", other.value)
        result = (self.value < other.value)
        self.log.info("result: %s", result)
        return result

    def __str__(self):
        """Return class name followed by string value in parentheses."""
        return "ComparisonLoggingWrapper(" + str(self.value) + ")"

    def __repr__(self):
        """Return constructor-like string."""
        return "ComparisonLoggingWrapper(" + repr(self.value) + ", " + repr(self.log) + ")"
