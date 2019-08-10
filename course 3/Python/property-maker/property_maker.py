#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from collections import Iterable


class PropertyMaker(type):
    """
    >>> class A(metaclass=PropertyMaker):
    ...     def get_x(self):
    ...         return 0
    ...
    >>> a = A()
    >>> a.x
    0
    >>> a.x = 11
    Traceback (most recent call last):
    ...
    AttributeError: can't set attribute
    >>> a.x
    0
    """
    def __call__(cls, *args, **kwargs):
        to_set = dict()
        to_get = dict()
        for attr in cls.__dict__:
            if attr.startswith('get_'):
                to_get[attr[4:]] = cls.__getattribute__(cls, attr)
            elif attr.startswith('set_'):
                to_set[attr[4:]] = cls.__getattribute__(cls, attr)
        normal_getattr = cls.__getattribute__
        normal_setattr = cls.__setattr__

        def getattr(self, key):
            print(key)
            if key in to_get:
                return to_get[key](self)
            else:
                return normal_getattr(self, key)

        def setattr(self, key, value):
            if key in to_set:
                to_set[key](self, value)
            elif key in to_get:
                raise AttributeError("can't set attribute")
            else:
                normal_setattr(self, key, value)

        cls.__getattribute__ = getattr
        cls.__setattr__ = setattr
        return type.__call__(cls, *args, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
