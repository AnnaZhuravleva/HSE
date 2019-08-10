#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
from copy import deepcopy


class ExtendedList(list):
    """
    >>> l = ExtendedList([1, 2, 3])
    >>> l.first
    1
    >>> l.F = 4
    >>> l
    [4, 2, 3]
    >>> l.size = 5
    >>> l.last = 100
    >>> l
    [4, 2, 3, None, 100]
    >>> l.size = 2
    >>> l
    [4, 2]
    >>> l.S = 0
    >>> l
    []
    """

    def __add__(self, other):
        self.append(other)

    def __getattribute__(self, item):
        if item is None:
            return
        if item == 'F' or item == 'first':
            return self[0]
        elif item == 'L' or item == 'last':
            return self[-1]
        elif item == 'R' or item == 'reversed':
            c = reversed(self)
            return list(c)
        elif item == 'S' or item == 'size':
            return len(self)
        else:
            return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        if key == 'F' or key == 'first':
            self[0] = value
        if key == 'L' or key == 'last':
            self[-1] = value
        if key == 'S' or key == 'size':
            if value > len(self):
                for i in range(value - len(self)):
                    self.append(None)
            else:
                for i in range(len(self) - value):
                    self.pop(-1)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
