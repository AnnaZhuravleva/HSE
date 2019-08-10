#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


def divisible(begin, end):
    """
    :param begin: int, positive integer
    :param end: int, positive integer
    :return: str, string of space separated integers

    Examples of usage:
    >>> divisible(1, 10)
    '7'
    >>> divisible(1, 17)
    '7 14'
    >>> len(divisible(100, 1000))
    407
    >>> divisible(29, 60)
    '42 49 56'
    >>> len(divisible(300, 3000).split())
    309
    >>> ns = [int(n) for n in divisible(300, 10000).split()]
    >>> seven_mask = [not bool(n % 7) for n in ns]
    >>> all(seven_mask)
    True
    >>> any(seven_mask)
    True
    >>> five_mask = [not bool(n % 5) for n in ns]
    >>> all(five_mask)
    False
    >>> any(five_mask)
    False
    >>> divisible(2, 5)
    ''
    >>> 1329 not in ns
    True
    """
    return ' '.join([str(v) for v in range(begin, end) if v % 7 == 0 and v % 5 != 0])


def register_count(string):
    """
    :param string: str, input string
    :return: dict, dict of lower and upper letter counts

    >>> register_count("Mama") == {'UPPER': 1, 'LOWER': 3}
    True
    >>> register_count("Your Name") == {'UPPER': 2, 'LOWER': 6}
    True
    >>> register_count("LingvoX!!!") == {'UPPER': 2, 'LOWER': 5}
    True
    >>> register_count("Trud, mir, mai! Zvahka!") == {'UPPER': 2, 'LOWER': 14}
    True
    >>> register_count("Coi ZIV!,,,,,") == {'UPPER': 4, 'LOWER': 2}
    True
    """
    lower = 0
    upper = 0
    for v in string:
        if v.islower():
            lower += 1
        elif v.isupper():
            upper += 1
    return {'UPPER': upper, 'LOWER': lower}


def pairwise_diff(first, second):
    """
    :param first: str, first input string
    :param second: str, second input string
    :return: float, percentage of different letters

    >>> pairwise_diff('ABSD', 'ABCD')
    0.25
    >>> pairwise_diff('aBSD', 'ABCD')
    0.5
    >>> pairwise_diff('LingvX', 'SpaceX')
    0.83
    >>> pairwise_diff('LingvoX', 'SpaceX')
    Traceback (most recent call last):
    ...
    AssertionError
    >>> pairwise_diff('abc', 'ab')
    Traceback (most recent call last):
    ...
    AssertionError
    >>> first = 'Salaman..'; second = 'Salaman.!'
    >>> round(1. / len(first), 2) == pairwise_diff(first, second)
    True
    >>> pairwise_diff(first + second, first + first)
    0.06
    >>> pairwise_diff(first * 3, second * 2 + first)
    0.07
    """
    assert len(first) == len(second)
    a = 0
    for i, j in zip(first, second):
        if i == j:
            a += 1
    return round(1 - a/len(first), 2)


def run_robot():
    """
    Uses input() inside.
    :return: int, rounded euclidean distance from origin
    """
    dirs = {"UP": 1, "DOWN": -1, "RIGHT": 1, "LEFT": -1}
    x, y = 0, 0
    while True:
        step = input()
        if not step:
            break
        step = step.split(' ')
        if step[0] == 'UP' or step[0] == 'DOWN':
            y += int(step[1])*dirs[step[0]]
        elif step[0] == 'LEFT' or step[0] == 'RIGHT':
            x += int(step[1])*dirs[step[0]]
        else:
            pass
    return round(math.sqrt((x*x + y*y)))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
