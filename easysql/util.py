def enforce_type(element, _type=str, exact=False):
    """
    Check if given `element` is an instance of `_type`.
    In case of `exact` checking, subclassing isn't allowed.
    """
    if not exact and isinstance(element, _type):
        return
    if exact and type(element) == _type:
        return

    raise TypeError(f"{element} has to be type {_type.__name__}. Is type {type(element)}")


def enforce_types(iterable, _type=str, exact=False, inner=True):
    """
    Make sure that every element and sub-element of
    given `iterable` is an instance of `_type`.
    In case of `exact` checking, subclassing isn't allowed.
    If `inner` is false, don't check sub-elements
    """
    for elem in iterable:
        try:
            enforce_type(elem, _type, exact)
        except TypeError as exc:
            if inner and hasattr(elem, "__iter__"):
                enforce_types(elem, _type, exact, inner)
            else:
                raise exc


def join(iterable, joiner=" "):
    return joiner.join(part for part in iterable if part != "")
