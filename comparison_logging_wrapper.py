"""Module that defines a wrapper object which logs comparisons."""

class ComparisonLoggingWrapper(object):
    """A wrapper for values which logs comparison operations"""

    def __init__(self, value, log):
        """Wrap the value using the log object."""
        self.value = value
        self.log = log

    def __cmp__(self, other):
        """Compare and log."""
        log.info("Called comparison on wrapped value: %s", self.value)
        try:
            other_value = other.value
            wrapped = True
        except AttributeError:
            other_value = other
            wrapped = False
        if wrapped:
            log.info("against wrapped value: %s", other_value)
        else:
            log.info("against bare value: %s", other_value)
        result = self.__cmp__(other_value)
        log.info("result: %s", result)
        return result
