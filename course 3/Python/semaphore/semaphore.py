#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class TooManyInstances(TypeError):
    pass


class InstanceSemaphore(type):
    """
    >>> class A(metaclass=InstanceSemaphore):
    ...     __max_instance_count__ = 2
    ...     def __init__(self, a):
    ...         self.a = a
    ...
    >>> one = A(1)
    >>> two = A(2)
    >>> three = A(3)
    Traceback (most recent call last):
        ...
    TooManyInstances: Too many instances. Expected 2.
    >>> three
    Traceback (most recent call last):
        ...
    NameError: name 'three' is not defined
    >>> del one
    >>> one
    Traceback (most recent call last):
        ...
    NameError: name 'one' is not defined
    >>> three = A(3)
    """
    count = 0

    def __new__(cls, *args, **kwargs):
        cls = type.__new__(cls, *args, **kwargs)
        cls.count = 0
        _init = cls.__init__
        cls.__max_instance_count__ = args[2]['__max_instance_count__']

        def _check(self, *args, **kwargs):
            cls.count += 1
            if cls.count > cls.__max_instance_count__:
                raise TooManyInstances('Too many instances. Expected {}.'.
                                       format(cls.__max_instance_count__))
            else:
                _init(self, *args, **kwargs)

        def _del(self):
            cls.count -= 1
            del self

        cls.__init__ = _check
        cls.__del__ = _del

        return cls


if __name__ == "__main__":
    import doctest
    doctest.testmod()
