#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date


class Person:
    """
    >>> p = Person('Ivan', 'Ivanov', 'male', date(1989, 4, 26))
    >>> print(p)
    Ivan Ivanov, male, 29 years

    >>> p.full_ages()
    29
    >>> Person('Ivan', 'Ivanov', 'man', "1989.4.26")
    Traceback (most recent call last):
        ...
    ValueError: bday must be date type
    """

    def __init__(self, name, surname, sex, bday):
        if not isinstance(bday, date):
            raise ValueError("bday must be date type")

        self.name = name
        self.surname = surname
        self.sex = sex
        self.bday = bday

    def full_ages(self):
        return (date.today() - self.bday).days // 365

    def __repr__(self):
        return f"{self.name} {self.surname}, {self.sex}, " \
            f"{self.full_ages()} years"

    def __eq__(self, other):
        return self.name == other.name and\
               self.surname == other.surname and\
               self.sex == other.sex and\
               self.bday == other.bday


class Student(Person):
    """
    >>> s = Student('Ivan', 'Ivanov', 'male', date(1989, 4, 26), 161, 9)
    >>> print(s)
    Ivan Ivanov, male, 29 years, 161 group, 9 skill
    """
    def __init__(self, name, surname, sex, bday, group, skill):
        super().__init__(
            name=name, surname=surname, sex=sex, bday=bday
        )
        self.group = group
        self.skill = skill

    def __repr__(self):
        repr_ = super().__repr__()
        repr_ += f", {self.group} group, {self.skill} skill"
        return repr_

    def __eq__(self, other):
        return super().__eq__(other) and\
               self.group == other.group and\
               self.skill == other.skill

    def __hash__(self):
        return hash(repr(self))


class Group:
    """
    Encapsulates list of students
    """
    def __init__(self, iterable):
        self._group = [s for s in iterable]

    def __repr__(self):
        group = [f"Student({i})" for i in self._group]
        return f"Group({group})"

    def __eq__(self, other):
        return isinstance(other, Group) and \
               set(self._group) == set(other._group)

    def sort_by_age(self, reverse=False):
        self._group.sort(key=lambda s: s.full_ages(), reverse=reverse)

    def sort_by_skill(self, reverse=False):
        self._group.sort(key=lambda s: s.skill, reverse=reverse)

    def sort_by_age_and_skill(self, reverse=False):
        self._group.sort(key=lambda s: (s.full_ages(), s.skill),
                         reverse=reverse)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
