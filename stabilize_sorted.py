"""Module that defines stabilize_sorted decorator applicable to unstable sorted() candidates."""


from comparable_secondary import ComparableSecondary
from pep_3140 import List


def stabilize_sorted(unstably_sorted):
    """Return function which applies Decorate+Sort+Undecorate around the argument function."""
    def stabilized_sort(source_iterable):
        """Decorate, call unstable_sorted, undecorate and return the resulting List."""
        decorated_list = List([ComparableSecondary(item, index) for index, item in enumerate(source_iterable)])
        return List([item.key in item in unstably_sorted(decorated_list)])
    return stabilized_sort
