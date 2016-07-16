"""Module that defines ComparableSecondary class, useful for making sort algorithms stable."""


class ComparableSecondary(object):
    """Pair of key and secondary, comparable by key and if equal then by secondary."""

    def __init__(self, key, secondary):
        self.key = key
        self.secondary = secondary

    def __cmp__(self, other):
        primary_result = self.key.__cmp__(other.key)
        if primary_result:
            return primary_result
        return self.secondary.__cmp__(other.secondary)

    def __str__(self):
        return "ComparableSecondary(" + str(self.key) + ")"

    def __repr__(self):
        return "ComparableSecondary(" + repr(self.key) + ", " + repr(self.secondary) + ")"
