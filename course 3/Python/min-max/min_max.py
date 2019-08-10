#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Iterable


def min_max(iterable, *args, key=None, cmp):
    if args and iterable:
        return sorted([iterable, sorted(args)[cmp]])[cmp]
    if not args:
        if not isinstance(iterable, Iterable):
            raise TypeError
        if key is not None:
            return sorted(iterable, key=lambda x: key(x))[cmp]
        return sorted(iterable)[cmp]
    return sorted(args)[cmp]


def min_max_rec(iterable, *args, key=None, cmp):
    s = []
    if not args:
        if not isinstance(iterable, Iterable):
            raise TypeError
        s = [e for e in iter(iterable)]
    else:
        s = [e for e in iter(args)]
        s.append(iterable)
    res = s[0]
    for i in s:
        if cmp == 0:
            if key is not None:
                if key(i) < key(res):
                    res = i
            elif key is None:
                if i < res:
                    res = i
        elif cmp == -1:
            if key is not None:
                if key(i) > key(res):
                    res = i
            elif key is None:
                if i > res:
                    res = i
    return res


def minimum(iterable, *args, key=None):
    """
    The same as built-in min (exclude default parameter).
    With a single iterable argument, return its smallest item. The
    default keyword-only argument specifies an object to return if
    the provided iterable is empty.

    >>> minimum(1, 2, 3) == min(1, 2, 3)
    True
    >>> minimum([1, 2, 3]) == min([1, 2, 3])
    True
    """
    return min_max_rec(iterable, *args, key=key, cmp=0)
    # return min_max(iterable, *args, key=key, cmp=0)


def maximum(iterable, *args, key=None):
    """
    The same as built-in max (exclude default parameter).
    With a single iterable argument, return its biggest item. The
    default keyword-only argument specifies an object to return if
    the provided iterable is empty.

    >>> maximum(1, 2, 3) == max(1, 2, 3)
    True
    >>> maximum([1, 2, 3]) == max([1, 2, 3])
    True
    """
    return min_max_rec(iterable, *args, key=key, cmp=-1)
    # return min_max(iterable, *args, key=key, cmp=-1)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
