#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Iterable, Iterator, Sequence
import inspect


class RangeIterator(Iterator):

    def __init__(self, rangeobj):
        self.rangeobj = rangeobj
        self.cur = self.rangeobj.start

    def __next__(self):
        a = self.cur
        self.cur += self.rangeobj.step
        if (self.rangeobj.step > 0 and a >= self.rangeobj.stop) or \
                (self.rangeobj.step < 0 and a <= self.rangeobj.stop):
            raise StopIteration()
        return a

    def __iter__(self):
        return self


class Range(Sequence, Iterable):

    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError(f"'{arg.__class__.__name__}'"
                                f" object cannot be interpreted as an integer")

        if len(args) == 1:
            self.start, self.stop, self.step = 0, args[0], 1
        elif len(args) == 2:
            self.start, self.stop, self.step = args[0], args[1], 1
        elif len(args) == 3:
            if args[2] == 0:
                raise ValueError('range() arg 3 must not be zero')
            self.start, self.stop, self.step = args[0], args[1], args[2]
        else:
            raise TypeError(f'range expected at most 3 arguments, '
                            f'got {len(args)}')

    def count(self, value):
        a = [1 for v in list(self.__iter__()) if value == v]
        return len(a)

    def index(self, value):
        idx = 0
        for a in list(self.__iter__()):
            if a == value:
                return idx
            idx += 1
        if not isinstance(value, int) and not isinstance(value, float) and \
                not isinstance(value, complex):
            raise ValueError('sequence.index(x): x not in sequence')
        if value >= self.__len__():
            raise ValueError(f'{value} is not in range')

    def __iter__(self):
        return RangeIterator(self)

    def __str__(self):
        if self.step == 1:
            return f'range({self.start}, {self.stop})'
        return f'range({self.start}, {self.stop}, {self.step})'

    __repr__ = __str__

    def __getitem__(self, key):
        if not isinstance(key, int) and not isinstance(key, slice):
            raise TypeError
        if isinstance(key, int):
            pos = self.start + self.step * key
            if (pos > self.stop > 0) or (pos < self.stop < 0):
                raise IndexError('range object index out of range')
            return pos
        if isinstance(key, slice):
            if key.start and abs(key.start) >= self.__len__() and \
                    key.stop and abs(key.stop) > self.__len__():
                return Range(0)
            a = list(self.__iter__())
            start = self.start
            stop = self.stop
            step = self.step
            if key.step:
                step *= key.step

            if (key.step and key.step > 0) or key.step is None:
                if key.start:
                    try:
                        start = a[key.start]
                    except IndexError:
                        start = a[-1]
                if key.stop:
                    try:
                        stop = a[key.stop]
                    except IndexError:
                        stop = self.start + self.__len__() * self.step

            if key.step and key.step < 0:
                if key.start:
                    try:
                        start = a[key.start]
                    except IndexError:
                        start = self.stop - 1
                else:
                    start = self.stop - int(self.stop / abs(self.stop))
                if key.stop:
                    try:
                        stop = a[key.stop]
                    except IndexError:
                        stop = self.start
                else:
                    stop = a[0] - int(self.stop / abs(self.stop))
            return Range(start, stop, step)

    def __len__(self):
        length = (self.stop - self.start) // self.step + \
                 bool((self.stop - self.start) % self.step)
        if length < 0:
            return 0
        return length

    def __contains__(self, value):
        for a in list(self.__iter__()):
            if a == value:
                return True
        return False

    def __eq__(self, other):
        return isinstance(other, Range) and\
               self.start == other.start and\
               self.stop == other.stop and\
               self.step == other.step


if __name__ == "__main__":
    import doctest
    doctest.testmod()
