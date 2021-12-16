"""Module that defines Interner class, de-duplicating equal objects."""

class Interner:
    """Interner implementation using dict."""

    def __init__(self, interned=None):
        """Set fields, empty set by default."""
        self.interned = dict() if interned is None else interned

    def intern(self, obj):
        """Intern if not already, return the interned value."""
        if obj not in self.interned:
            self.interned[obj] = obj
        return self.interned[obj]

    def __str__(self):
        """Return class name with dict in parentheses."""
        return "Interner(" + str(self.interned) + ")"

    def __repr__(self):
        """Return constructor-like string."""
        return "Interner(interned=" + repr(self.interned) + ")"
