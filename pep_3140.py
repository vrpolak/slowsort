def list_str(iterable):
    """Workaround for, PEP 3140 to use instead of str()"""
    return str([str(item) for item in iterable])
