#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect


class FieldInitializer(type):
    """
    >>> class A(metaclass=FieldInitializer):
    ...     def __init__(self, a, b, c=1):
    ...         self.a = a
    ...         self.b = b
    ...         self.c = c
    ...
    >>> a = A(a=1, b=2, c=11, foo=4)
    >>> a.a
    1
    >>> a.b
    2
    >>> a.c
    11
    >>> a.foo
    4
    """

    def __call__(cls, *args, **kwargs):
        kw = inspect.getfullargspec(cls.__init__).args
        init_kwargs = {k: v for k, v in kwargs.items() if k in kw}
        instance = type.__call__(cls, *args, **init_kwargs)
        for key, value in kwargs.items():
            if not hasattr(instance, key):
                setattr(instance, key, value)
        return instance


if __name__ == "__main__":
    import doctest
    doctest.testmod()
