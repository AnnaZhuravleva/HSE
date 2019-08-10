#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import Iterable, Iterator, Sequence


class RangeIterator(Iterator):

    def __init__(self, rangeobj):
        self.rangeobj = rangeobj
        self.cur = self.rangeobj.start

    def __next__(self):
        a = self.cur
        self.cur += self.rangeobj.step
        if (self.rangeobj.step > 0 and a >= self.rangeobj.stop) or\
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

    def __eq__(self, other):
        return isinstance(other, Range) and\
               self.start == other.start and\
               self.stop == other.stop and\
               self.step == other.step

    def __iter__(self):
        return RangeIterator(self)

    def __repr__(self):
        if self.step == 1:
            return f'range({self.start}, {self.stop})'
        return f'range({self.start}, {self.stop}, {self.step})'

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError
        pos = self.start + self.step * key
        if (pos > self.stop > 0) or (pos < self.stop < 0):
            raise IndexError('range object index out of range')
        return pos

    def __len__(self):
        length = (self.stop - self.start) // self.step +\
            bool((self.stop - self.start) % self.step)
        if length < 0:
            return 0
        return length

    def __contains__(self, value):
        delta = value - self.start
        a, b = divmod(delta, self.step)
        return b == 0 and 0 <= a < len(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    b = Range(10, 13)
    print(list(Range(10)), 3 in b)
