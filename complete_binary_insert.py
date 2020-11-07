"""Module that defines binary insert operation using complete pivoting strategy."""

from pluggable_binary_insert import mutating_pluggable_binary_insert


def complete_pivot(lower_index, upper_index):
    """Return index strictly between bondaries.

    Choose the pivot in such a way, that level of leafs of the equivalent
    binary search tree increases, but not over more than one level.
    In other words, it should be a complete binary tree
    https://xlinux.nist.gov/dads//HTML/completeBinaryTree.html
    where "left" means "towards higher indexes".

    TODO: Figure out a more specific adjective than "complete".
    """
    spread = upper_index - lower_index
    assert spread >= 2
    lesser_whole = 1 << (len(bin(spread)) - 3)
    complement_whole = spread - lesser_whole
    if not complement_whole:
        # Full tree. Fairly common, least lucky, but effective case in Ford-Johnson.
        return lower_index + spread // 2
    lesser_half = lesser_whole >> 1
    if complement_whole >= lesser_half:
        # Few shorter paths on lower scale, common case especially for longer insertion targets.
        return lower_index + complement_whole
    else:
        # Very rare case.
        return lower_index + lesser_half


def mutating_complete_binary_insert(element, target, lower_index, upper_index):
    """Binary insertion using complete_pilot plugged to pluggable_binary_insert."""
    mutating_pluggable_binary_insert(complete_pivot, element, target, lower_index, upper_index)
