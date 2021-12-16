"""Module that defines a wrapper object asks user for comparisons.

This uses functools to generate rich comparison functions.
Equivalence test does not ask, as sorts never do equal test directly.
"""

from functools import total_ordering


@total_ordering
class InteractiveComparisonWrapper(object):
    """A wrapper which asks user via console."""

    def __init__(self, value):
        """Wrap the value, it is to be used as an identifier for user."""
        self.value = value

    def __eq__(self, other):
        """Equality test, no user input needed."""
        return self.value == other.value

    def __lt__(self, other):
        """Less-than test, asking user."""
        print(f"First: {self.value}")
        print(f"Second: {other.value}")
        while 1:
            resp = input("Is the first one less than the second one? ")
            if resp:
                break
        result = resp.lower() in ("y", "yes", "1", "true", "is", "it is")
        print(f"'less than' result: {result}")
        return result

    def __str__(self):
        """Return class name followed by string value in parentheses."""
        return f"InteractiveComparisonWrapper({self.value})"

    def __repr__(self):
        """Return constructor-like string."""
        return f"InteractiveComparisonWrapper({self.value!r})"

    def __hash__(self):
        """Return hash so wrapped items can be put in a set or similar."""
        return hash(str(self))
