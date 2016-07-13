"""Module that defines Ford-Johnson sortin algorithm."""

# FIXME: Finish writing implementation.

class ComparablePayload(object):
    """Pair of key and payload, comparable by key. Can be used to store sorted pairs."""

    def __init__(self, key, payload):
        self.key = key
        self.payload = payload

    def __cmp__(self, other):
        return self.key.__cmp__(other.key)

    def __str__(self):
        return "ComparablePayload(" + str(self.key) + ")"

    def __repr__(self):
        return "ComparablePayload(" + repr(self.key) + ", " + repr(self.payload) + ")"


def binary_insert(element, target, lower_index, upper_index):
    """Insert element into target list.
    Lower index is confirmed to be before, can be -1;
    Upper index is confirmed to be after, can be len(target)."""
    window_size = upper_index - lower_index
    assert window_size > 0, "Binary insert encountered non-positive window size."
    if window_size <= 1:
        if lower_index < 0:
            result = [element]
            result.extend(target)
            return result
        result = target[:lower_index + 1]
        result.append(element)
        if upper_index < len(target):
            result.extend(target[upper_index:])
        return result
    critical_index = lower_index + window_size / 2
    if element < target[critical_index]:
        return binary_insert(element, target, lower_index, critical_index)
    else:
        return binary_insert(element, target, critical_index, upper_index)


def ford_johnson_sort_destructive(source):
    """Form pairs and sort them according to top elements (odd element at the end).
    Binary-insert dangling elements in an order that maximizes efficiency.

    Source should support len(), pop(), and element should support comparison."""
    if len(source) < 2:
        return source
    pairs = []
    while len(source) > 1:
        former = source.pop()
        latter = source.pop()
        if former > latter:
            pairs.append(ComparablePayload(former, latter))
        else:
            pairs.append(ComparablePayload(latter, former))
    pairs = ford_johnson_sort_destructive(pairs)
    len_pairs = len(pairs)
    # Additional index value is needed for localizing anchors.
    first_pair = pairs[0]
    first_item = ComparablePayload(first_pair.payload, 0)
    second_item = ComparablePayload(first_pair.key, 0)
    insertion_target = [first_item, second_item]
    jacobsthal_previous = 1
    jacobsthal_current = 1
    while jacobsthal_current < len_pairs:
        jacobsthal_backup = jacobsthal_previous
        jacobsthal_previous = jacobsthal_current
        jacobsthal_current = jacobsthal_previous + 2 * jacobsthal_backup
        if jacobsthal_current > len_pairs:
            jacobsthal_backup = jacobsthal_current
            jacobsthal_current = len_pairs
        for index in range(len_pairs)[jacobsthal_previous:jacobsthal_current]:
            pair = pairs[index]
            insertion_target.append(ComparablePayload(pair.key, index))
        if jacobsthal_backup > len_pairs:
            # We have a leeway, we can discount the cost of inserting the odd element.
            if len(source):
                odd = ComparablePayload(source.pop(), 0)
                insertion_target = binary_insert(odd, insertion_target, -1, len(insertion_target))
        upper_index = len(insertion_target) - 1
        for index in range(len_pairs)[jacobsthal_current - 1:jacobsthal_previous - 1:-1]:
            pair = pairs[index]
            while insertion_target[upper_index].payload is not index:
                upper_index -= 1
                assert upper_index >= 0
            item = ComparablePayload(pair.payload, 0)
            insertion_target = binary_insert(item, insertion_target, -1, upper_index)
    # Index value is no longer needed.
    for index in range(len(insertion_target)):
        insertion_target[index] = insertion_target[index].key
    if len(source):
        odd = source.pop()
        insertion_target = binary_insert(odd, insertion_target, -1, len(insertion_target))
    # print "sorted", [str(item) for item in insertion_target]  # PEP 3140
    return insertion_target


def ford_johnson_sort(source):
    """Copy iterable source to a list and apply destructive sort. Return the result."""
    return ford_johnson_sort_destructive(list(source))


def ford_johnson_sort_tuples(source):
    """Adapter for sorting tuples by [1] element."""
    cp_source = [ComparablePayload(item[1], item) for item in source]
    cp_result = ford_johnson_sort(cp_source)
    result = [item.payload for item in cp_result]
    return result
