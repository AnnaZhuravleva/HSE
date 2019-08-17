#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import MutableMapping, OrderedDict
import functools

# is not implemented


class LoggerMixin(object):

    def __init__(self):
        self.cache = {}

    def __getattribute__(self, item):
        tmp = []
        x = object.__getattribute__(self, item)

        def wrapper(*args, **kwargs):
            s = f'Called {item}(). args: {args}, kwargs: {kwargs}, ' \
                f'return: {x(*args, **kwargs)}'
            tmp.append(s)
            return x(*args, **kwargs)
        return wrapper

    def __str__(self):
        return ''


class Test(LoggerMixin):
    """
    >>> t = Test()
    >>> t.test(1, 2, c=22)
    25
    >>> t.test(17, 2, c=12)
    31
    >>> print(t)
    Called test(). args: (1, 2), kwargs: {'c': 22}, return: 25
    Called test(). args: (17, 2), kwargs: {'c': 12}, return: 31
    """

    def test(self, a, b, c=None):
        return a + b + c


if __name__ == '__main__':
    t = Test()
    print(t.test(10, 20, 53))
    print(t)
    # import doctest
    # doctest.testmod()
