"""Module that defines binary insert operation using pluggable pivoting strategy."""


def pluggable_binary_insert(choose_pivot, element, target, lower_index, upper_index):
    """Insert element into target list.
    Lower index is confirmed to be before, can be -1;
    Upper index is confirmed to be after, can be len(target).

    Pivot element is chosen by calling choose_pivot(lower_index, upper_index).
    # TODO: Will there be pivoting strategies depending on more than just spread?

    In case of tie, element is inseted to upper part."""
    spread = upper_index - lower_index
    assert spread > 0, "Binary insert encountered non-positive window size."
    if spread <= 1:
        target[upper_index:upper_index] = [element]
        return target
    pivot_index = choose_pivot(lower_index, upper_index)
    if element < target[pivot_index]:
        return pluggable_binary_insert(choose_pivot, element, target, lower_index, pivot_index)
    else:
        return pluggable_binary_insert(choose_pivot, element, target, pivot_index, upper_index)

