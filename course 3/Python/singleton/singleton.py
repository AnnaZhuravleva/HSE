#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools


def singleton(cls):
    """
    >>> @singleton
    ... class A:
    ...     pass

    >>> id(A()) == id(A()) == id(A())
    True
    """

    instance = None

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):

        nonlocal instance

        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod()
