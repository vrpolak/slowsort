"""Module that defines binary insert operation using halving pivoting strategy."""


from pluggable_binary_insert import pluggable_binary_insert


def halving_pivot(lower_index, upper_index):
    """Return index strictly between bondaries.
    Choose the exact middle, of lower of two most middle indexes."""
    spread = upper_index - lower_index
    assert spread >= 2
    return lower_index + spread / 2


def halving_binary_insert(element, target, lower_index, upper_index):
    """Binary insertion using halving_pilot plugged to pluggable_binary_insert."""
    return pluggable_binary_insert(halving_pivot, element, target, lower_index, upper_index)
