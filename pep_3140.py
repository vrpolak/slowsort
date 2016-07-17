"""Module providing few iterable types with str() respecting PEP 3140.

FIXME: Guard against possible cycles in graphs of references."""


from collections import deque


class List(list):
    """A list with str support."""

    def __str__(self):
        """Return comma+space separated str of items in square brackets."""
        if not self:
            return "[]"
        substr_list = []
        for item in self:
            substr_list.append(", ")
            substr_list.append(str(item))
        substr_list.append("]")
        substr_list[0] = "["
        return "".join(substr_list)


class Tuple(tuple):
    """A tuple with str support."""

    def __str__(self):
        """Return comma+space separated str of items in round brackets."""
        if not self:
            return "()"
        substr_list = []
        for item in self:
            substr_list.append(", ")
            substr_list.append(str(item))
        substr_list.append(")")
        substr_list[0] = "("
        return "".join(substr_list)


class Dict(dict):
    """A dict with str support."""

    def __str__(self):
        """Return comma+space separated str of items in curly brackets."""
        if not self:
            return "{}"
        substr_list = []
        for key, value in self.items():
            substr_list.append(", ")
            substr_list.append(str(key))
            substr_list.append(": ")
            substr_list.append(str(value))
        substr_list.append("}")
        substr_list[0] = "{"
        return "".join(substr_list)


class Deque(deque):
    """A deque with str support."""

    def __str__(self):
        """Return str of List corresponding to self."""
        # TODO: What about "Deque([1, 2, ...])"?
        return str(List(self))
