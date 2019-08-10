#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools


def cached(func):  # correct signature is not known
    """
    >>> @cached
    ... def add(a, b):
    ...     print(a, b)
    ...     return a + b
    ...
    >>> add(1, 2)
    1 2
    3
    >>> add(1, 2)
    3
    >>> add(2, 2)
    2 2
    4
    >>> add(2, 2)
    4
    """
    cach = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        values = (args, tuple(sorted(kwargs.items())))
        if values not in cach:
            cach[values] = func(*args, **kwargs)
        return cach[values]

    return wrapper


if __name__ == '__main__':
    import doctest
    doctest.testmod()
