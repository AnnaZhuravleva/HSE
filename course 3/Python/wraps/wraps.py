#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def wraps(*args):  # correct signature is not known
    """
    >>> def decorator(func):
    ...     @wraps(func)
    ...     def wrapper(*args, **kwargs):
    ...         return func(*args, **kwargs)
    ...     return wrapper

    >>> @decorator
    ... def foo(x):
    ...     \"\"\"Docstring foo\"\"\"
    ...     return x

    >>> foo("test")
    'test'
    >>> foo.__doc__
    'Docstring foo'
    >>> foo.__name__
    'foo'
    >>> foo.__module__
    '__main__'
    """
    def inner(func):
        return func(*args)
    return inner


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@decorator
def foo(x):
    """Docstring foo"""
    return x


if __name__ == "__main__":
    import doctest
    doctest.testmod()
