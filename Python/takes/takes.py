#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def takes(*types):
    """
       >>> @takes(int, str, float, int)
       ... def foo(*args):
       ...     print(args)

       >>> try:
       ...     args = 1, "arg1", 2.0, 11
       ...     foo(*args)
       ... except TypeError as exc:
       ...     print(str(exc))
       (1, 'arg1', 2.0, 11)

       >>> @takes(int, float, str, int)
       ... def bar(*args):
       ...     print(args)

       >>> try:
       ...     args = 1, "arg1", "kek", 12.0
       ...     foo(*args)
       ... except TypeError as exc:
       ...     print(str(exc))
       str argument in position 2 is not float object
       """

    def wrapper(f):
        def inner(*args):
            for k, (arg, type_) in enumerate(zip(args, types)):
                if not isinstance(arg, type_):
                    raise TypeError(f'{arg.__class__.__name__} '
                                    f'argument in position {k} '
                                    f'is not {type_.__name__} object')
            return f(*args)
        return inner
    return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod()
