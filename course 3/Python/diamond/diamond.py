#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class A:
    _init = 0

    def __init__(self, a, **kwargs):
        A._init += 1
        self.a = a
        for key, value in kwargs.items():
            setattr(self, key, value)


class B(A):
    _init = 0

    def __init__(self, b1, b2, *args, **kwargs):
        B._init += 1
        super().__init__(*args, **kwargs)
        self.b1 = b1
        self.b2 = b2


class C(A):
    _init = 0

    def __init__(self, c1, c2, *args, **kwargs):
        C._init += 1
        super().__init__(*args, **kwargs)
        self.c1 = c1
        self.c2 = c2


class D(B, C):
    _init = 0

    def __init__(self, d1, d2, *args, **kwargs):
        D._init += 1
        super().__init__(*args, **kwargs)
        self.d1 = d1
        self.d2 = d2


if __name__ == "__main__":
    main()
