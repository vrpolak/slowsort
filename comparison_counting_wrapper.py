"""Module that defines a wrapper object which counts comparisons."""

class SimpleCounter(object):
    """A simple counter to use."""

    def __init__(self):
        """Initialization."""
        self.count = 0

class ComparisonCountingWrapper(object):
    """A wrapper for values which counts comparison operations"""

    def __init__(self, value, counter):
        """Wrap the value using the log object."""
        self.value = value
        self.counter = counter

    def __cmp__(self, other):
        """Compare and increment counter."""
        try:
            other_value = other.value
            wrapped = True
        except AttributeError:
            other_value = other
            wrapped = False
        self.counter.count += 1
        result = self.value.__cmp__(other_value)
        return result
