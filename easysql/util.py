def check_has_not_type(iterable, obj=str):
    for elem in iterable:
        if type(elem) == obj:
            continue
        elif hasattr(elem, "__iter__"):
            check_has_not_type(elem, obj)
        elif type(elem) != obj:
            raise TypeError(
                "{} has to be type {}. Is type {}".format(
                    elem, obj.__name__, type(elem)
                )
            )


def join(iterable, joiner=" "):
    return joiner.join([part for part in iterable if part != ""])
