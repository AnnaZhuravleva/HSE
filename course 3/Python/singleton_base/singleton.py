#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


if __name__ == "__main__":
    import doctest
    doctest.testmod()
