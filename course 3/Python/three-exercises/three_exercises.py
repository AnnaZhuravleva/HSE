#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import contextlib
from contextlib import contextmanager
import sys
import traceback


class supresser:
    """
    Context manager supresses all exceptions with specified types

    >>> with supresser(ZeroDivisionError):
    ...     print("OK")
    ...     1/0
    ...
    OK
    """
    def __init__(self, *types_):
        self.types_ = types_

    def __enter__(self):
        if Exception in self.types_:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True


class retyper:
    """
        Context manager changes type of exception to another type, saves
        all attributes (args and __traceback__). And raises new exception again

        >>> try:
        ...     with retyper(ValueError, TypeError):
        ...         raise ValueError("wrong cast")
        ... except TypeError as e:
        ...     print(e.args[0])
        ...
        wrong cast
        """
    def __init__(self, type_from, type_to):
        self.type_from = type_from
        self.type_to = type_to

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == self.type_from:
            raise self.type_to(exc_val)


class dumper:
    """
    Context manager dumps an exception to stream
    (dumps value and traceback of exception). Stream object must implement
    write() method. Then raises exception again

    >>> with open("dump.txt", 'w') as s, dumper(stream=s):
    ...     raise LookupError("lookup error")
    ...
    Traceback (most recent call last):
    ...
    LookupError: lookup error
    """
    def __init__(self, stream=None):
        self.stream = stream

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.write(traceback.format_exc())
        raise


if __name__ == "__main__":
    import doctest
    doctest.testmod()
