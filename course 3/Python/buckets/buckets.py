#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Buckets:

    def __init__(self, length, default):
        self.default = default
        self.buckets = [default] * length


    def add(self, index, element):
        self.buckets[index].append(element)

    def find(self, index, element):
        return element in self.buckets[index]

    def clear(self, index):
        self.buckets[index] = self.default


if __name__ == "__main__":
    import doctest
    doctest.testmod()
