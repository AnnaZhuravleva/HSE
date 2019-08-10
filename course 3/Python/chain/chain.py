#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Iterable


def chain(*args):
    """
    >>> list(chain([["test"]]))
    ['t', 'e', 's', 't']
    """
    for item in args:
        try:
            for i in item:
                if i != item:
                    yield from chain(i)
                else:
                    yield i
        except TypeError:
            yield item


if __name__ == "__main__":
    import doctest
    doctest.testmod()
