#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List
from numbers import Number


def regexp_0(text: str, pattern: str) -> List[slice]:
    """
    Finds the occurrence and position of the substrings within a string

    >>> regexp_0("LingvoX SpaceX SpacoX", "oX")
    [slice(5, 7, None), slice(19, 21, None)]
    """
    m = []
    for i in range(len(text)):
        try:
            sl = re.match(pattern, text[i:]).span()
            m.append(slice(sl[0] + i, sl[1] + i, None))
        except AttributeError:
            pass
    return m


def regexp_1(text: str) -> str:
    """
    Converts camel case string to snake case string

    >>> regexp_1("QObject")
    'q_object'

    >>> regexp_1("KNeighborsClassifier")
    'k_neighbors_classifier'
    """
    for i in range(len(text)):
        try:
            if re.match('[A-ZА-Я]{2}', text[i:]) is not None:
                a = (re.match('[A-ZА-Я]{2}', text[i:])).group()
                b = a[0] + '_' + a[1]
            elif re.match('[a-zа-я][A-ZА-Я]', text[i:]) is not None:
                a = (re.match('[a-zа-я][A-ZА-Я]', text[i:])).group()
                b = a[0] + '_' + a[1]
            else:
                a = b = text[i]
            text = re.sub(a, b.lower(), text)
        except AttributeError:
            pass
    return text


def regexp_2(text: str, length: int) -> str:
    """
    Removes words from a string of length between 1 and a given number

    >>> regexp_2("Hello Cyril Kak dela bro", 3)
    'Hello Cyril dela'

    >>> regexp_2("Hello Cyril Kak dela bro", 4)
    'Hello Cyril'
    """
    return re.sub(r'\s?\b\w{1,' + str(length) + r'}\b\s*?', '', text)


def regexp_3(text: str) -> str:
    """
    Removes the parenthesis area in a string

    >>> regexp_3("Polina (Ivan)")
    'Polina'

    >>> regexp_3("Mark (Station) (LingvoX)")
    'Mark'
    """
    return re.sub(r'\s?\(.*\)', '', text)


def regexp_4(num: Number) -> bool:
    """
    Returns true whenever a decimal with a precision of 2

    >>> regexp_4(1.22)
    True
    >>> regexp_4(1.2)
    True
    >>> regexp_4(11)
    True
    >>> regexp_4(11.)
    True
    >>> regexp_4(11.333)
    False
    """
    try:
        return len(re.split(r'\.', str(num))[1]) <= 2
    except IndexError:
        return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
