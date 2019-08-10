#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def map_(func, iterable):
    """
    The same as built-in map(), but generator

    >>> from collections import Generator
    >>> square = lambda x: x ** 2
    >>> isinstance(map_(square, range(10)), Generator)
    True
    >>> list(map_(square, range(10)))
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    """
    for i in iterable:
        yield func(i)


def zip_(*iterables):
    """
    The same as built-in zip(), but generator

    >>> for i, j, k in zip_(range(3), range(4), range(-7, 0)):
    ...     print(i*i, j*j, k*k)
    0 0 49
    1 1 36
    4 4 25

    """
    p = 0
    while True:
        try:
            res = [i[p] for i in iterables]
            p += 1
            yield res
        except IndexError:
            break


def dropwhile(predicate, iterable):
    """
    The same as itertools.dropwhile(), but generator

    >>> from collections import Generator
    >>> isinstance(dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1]), Generator)
    True
    >>> list(dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1]))
    [6, 4, 1]
    """
    while predicate(iterable[0]):
        iterable.pop(0)
    for i in iterable:
        yield i


def filterfalse(predicate, iterable):
    """
    The same as itertools.filterfalse(), but generator

    >>> from collections import Generator
    >>> isinstance(filterfalse(lambda x: x % 2, range(10)), Generator)
    True
    >>> list(filterfalse(lambda x: x % 2, range(10)))
    [0, 2, 4, 6, 8]
    """
    if predicate is None:
        predicate = bool
    for i in iterable:
        if not predicate(i):
            yield i


def unique(iterable):
    """
    Generates unique values from iterable object

    >>> from collections import Generator
    >>> isinstance(unique(range(10)), Generator)
    True
    >>> list(unique([1, 1, 2, 2, 3, 1, 11, -1]))
    [1, 2, 3, 11, -1]
    """
    unique = []
    for i in iterable:
        if i not in unique:
            yield i
            unique.append(i)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
