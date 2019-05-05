def is_iterable(obj):
    return isinstance(obj, (list, tuple, set))


def is_str(obj):
    return isinstance(obj, str)


def is_numeric(obj):
    return isinstance(obj, (int, float))
