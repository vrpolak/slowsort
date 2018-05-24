"""Module that defines ComparableSecondary class, useful for making sort algorithms stable."""

from functools import total_ordering


@total_ordering
class ComparableSecondary(object):
    """Pair of key and secondary, comparable by key and if equal then by secondary."""

    def __init__(self, key, secondary):
        """Wrap key and secondary into a sigle object."""
        self.key = key
        self.secondary = secondary

    def __eq__(self, other):
        """Equality test, test secondaries only if keys are the same.."""
        return False if (self.key == other.key) else (self.secondary == other.secondary)

    def __lt__(self, other):
        """Less-than test, test secondaries only if keys are the same."""
        keys_inequal = not (self.key == other.key)
        return (self.key < other.key) if not (self.key == other.key) else (self.secondary < other.secondary)

    def __str__(self):
        """Return class name followed by string key in parentheses."""
        return "ComparableSecondary(" + str(self.key) + ")"

    def __repr__(self):
        """Return constructor-like string."""
        return "ComparableSecondary(" + repr(self.key) + ", " + repr(self.secondary) + ")"
