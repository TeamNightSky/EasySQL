def check_has_not_type(iterable, obj=str):
    for elem in iterable:
        if type(elem) == obj:
            continue
        elif hasattr(elem, "__iter__"):
            check_has_not_type(elem, obj)
        elif type(elem) != obj:
            raise TypeError(f"{elem} has to be type {obj.__name__}. Is type {type(elem)}")


def join(iterable, joiner=" "):
    return joiner.join([part for part in iterable if part != ""])
