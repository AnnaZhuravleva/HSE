#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy


class Transaction:

    def __init__(self, storage):
        self.storage = storage
        self.copy = deepcopy(storage._data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type or exc_value:
            raise
        else:
            self.storage._data = self.copy
            return True

    def __setitem__(self, key, value):
        self.copy[key] = value

    def __getitem__(self, key):
        return self.copy[key]

    def __delitem__(self, key):
        del self.copy[key]


class Storage:
    """

    >>> try:
    ...     s = Storage()
    ...     with s.edit() as e:
    ...         e['a'] = 1
    ...         1/0
    ...     print(s['a'])
    ... except ZeroDivisionError:
    ...     print(s['a'])
    Traceback (most recent call last):
    ...
    KeyError: 'a'
    """

    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def edit(self):
        return Transaction(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
