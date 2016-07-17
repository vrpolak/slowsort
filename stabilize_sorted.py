"""Module that defines stabilize_sorted decorator applicable to unstable sorted() candidates."""


from comparable_secondary import ComparableSecondary
from pep_3140 import List


def stabilize_sorted(unstably_sorted):
    """Return function which applies Decorate+Sort+Undecorate around the argument function."""

    def stabilized_sorted(source_iterable):
        """Decorate, call unstable_sorted, undecorate and return the resulting List."""
        decorated_list = List([ComparableSecondary(key, index) for index, key in enumerate(source_iterable)])
        return List([item.key for item in unstably_sorted(decorated_list)])

    return stabilized_sorted


def stabilize_pluggable_sorted(pluggable_unstably_sorted):
    """Return function which applies Decorate+Sort+Undecorate around the argument function."""

    def stabilized_pluggable_sorted(plugin, source_iterable):
        """Decorate, call unstable_sorted, undecorate and return the resulting List."""
        decorated_list = List([ComparableSecondary(key, index) for index, key in enumerate(source_iterable)])
        return List([item.key for item in pluggable_unstably_sorted(plugin, decorated_list)])

    return stabilized_pluggable_sorted
