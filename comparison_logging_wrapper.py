"""Module that defines a wrapper object which logs comparisons."""

class ComparisonLoggingWrapper(object):
    """A wrapper for values which logs comparison operations"""

    def __init__(self, value, log):
        """Wrap the value using the log object."""
        self.value = value
        self.log = log

    def __cmp__(self, other):
        """Compare and log."""
        self.log.info("Called comparison on wrapped value: %s", self.value)
        try:
            other_value = other.value
            wrapped = True
        except AttributeError:
            other_value = other
            wrapped = False
        if wrapped:
            self.log.info("against wrapped value: %s", other_value)
        else:
            self.log.info("against bare value: %s", other_value)
        result = self.value.__cmp__(other_value)
        self.log.info("result: %s", result)
        return result

    def __str__(self):
        return "ComparisonLoggingWrapper(" + str(self.value) + ", " + str(self.log) + ")"

    def __repr__(self):
        return "ComparisonLoggingWrapper(" + repr(self.value) + ", " + repr(self.log) + ")"
