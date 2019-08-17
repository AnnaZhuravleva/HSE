#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from datetime import date
from copy import deepcopy
from collections import Iterable
from itertools import permutations
import string

try:
    from sol_group import Person, Student, Group
except (ModuleNotFoundError, ImportError):
    from group import Person, Student, Group


class TestPerson(unittest.TestCase):

    @staticmethod
    def _get_polina():
        return Person(
            "Polina", "Gagarina",
            "female", date(1990, 4, 12)
        )

    def test_init(self):
        p = self._get_polina()

        self.assertTrue(hasattr(p, "name"))
        self.assertTrue(hasattr(p, "surname"))
        self.assertTrue(hasattr(p, "sex"))
        self.assertTrue(hasattr(p, "bday"))

        with self.assertRaises(ValueError):
            Person("a", "b", "c", "1990/4/12")

        with self.assertRaises(ValueError):
            Person("a", "b", "c", 1990)

        with self.assertRaises(ValueError):
            Person("a", "b", "c", [])

    def test_ages(self):
        p = self._get_polina()

        self.assertTrue(hasattr(p, "full_ages"))
        self.assertEqual(p.full_ages(), 29)

        for i in range(10):
            p.bday = date(1990 + i, 4, 12)
            self.assertEqual(p.full_ages(), 29 - i, i)

    def test_eq(self):

        p = self._get_polina()
        self.assertEqual(p, p)
        self.assertNotEqual(
            p, Person("Polina", "Gagarina", "female", date(1992, 4, 12))
        )
        self.assertNotEqual(
            p, Person("Polina", "Gagarina", "male", date(1990, 4, 12))
        )
        self.assertNotEqual(
            p, Person("Polina", "Mareeva", "female", date(1990, 4, 12))
        )
        self.assertNotEqual(
            p, Person("Nadya", "Gagarina", "female", date(1990, 4, 12))
        )
        self.assertNotEqual(
            p, Person("Katya", "Gagarina", "female", date(1990, 4, 12))
        )
        self.assertNotEqual(
            p, Person("Mark", "Sobolev", "male", date(1999, 4, 12))
        )

    def test_str(self):

        p = self._get_polina()
        self.assertEqual(
            str(p), "Polina Gagarina, female, 29 years"
        )
        p = Person('Ivan', 'Ivanov', 'male', date(1989, 4, 26))
        self.assertEqual(
            str(p),
            "Ivan Ivanov, male, 30 years"
        )
        self.assertEqual(
            Person('A', 'B', 'male', date(1989, 4, 26)).__str__(),
            "A B, male, 30 years"
        )
        self.assertEqual(
            str(Person('Cap', 'Ter', 'male', date(1989, 4, 26))),
            "Cap Ter, male, 30 years"
        )
        for c in string.printable:
            p.name = c + c
            p.surname = c
            self.assertEqual(
                str(p),
                f"{c + c} {c}, male, 30 years"
            )


class TestStudent(unittest.TestCase):

    @staticmethod
    def _get_galina():
        return Student(
            "Galina", "Moskovskaya",
            "female", date(1992, 4, 12),
            161, 5
        )

    def test_inheritance(self):

        self.assertTrue(issubclass(Student, Person))
        self.assertTrue('full_ages()' not in Student.__dict__)

    def test_init(self):
        p = self._get_galina()
        self.assertTrue(hasattr(p, "group"))
        self.assertTrue(hasattr(p, "skill"))

        with self.assertRaises(ValueError):
            Student("a", "b", "c", "1990/4/12", 1, 1)

        with self.assertRaises(ValueError):
            Student("a", "b", "c", 1990, 1, 1)

        with self.assertRaises(ValueError):
            Student("a", "b", "c", [], 1, 1)

    def test_str(self):
        s = self._get_galina()
        self.assertEqual(
            str(s), "Galina Moskovskaya, female, 27 years, 161 group, 5 skill"
        )
        s = Student('Ivan', 'Ivanov', 'male', date(1989, 4, 26), 1, 1)
        self.assertEqual(
            str(s),
            "Ivan Ivanov, male, 30 years, 1 group, 1 skill"
        )
        self.assertEqual(
            Student('A', 'B', 'male', date(1989, 4, 26), 1, 2).__str__(),
            "A B, male, 30 years, 1 group, 2 skill"
        )
        self.assertEqual(
            str(Student('Cap', 'Ter', 'male', date(1989, 4, 26), 11, 3)),
            "Cap Ter, male, 30 years, 11 group, 3 skill"
        )
        for i, c in enumerate(string.printable):
            s.name = c + c
            s.surname = c
            s.skill = i
            self.assertEqual(
                str(s),
                f"{c + c} {c}, male, 30 years, 1 group, {i} skill"
            )

    def test_eq(self):
        s = self._get_galina()
        self.assertEqual(s, s)

        self.assertNotEqual(
            s, Student(
                "Galina", "Moskovskaya",
                "female", date(1992, 4, 12), 161, 6
            )
        )
        self.assertNotEqual(
            s, Student("Galina", "A", "female", date(1992, 4, 12), 161, 5)
        )
        self.assertNotEqual(
            s, Student(
                "Galina", "Moskovskaya",
                "female", date(1992, 4, 11), 11, 6)
        )
        self.assertNotEqual(
            s, Student(
                "Galina", "Moskovskaya",
                "female", date(1992, 2, 12), 161, 6
            )
        )
        self.assertNotEqual(
            s, Student(
                "Galina", "Moskovskaya",
                "female", date(1992, 4, 12), 162, 6
            )
        )
        self.assertNotEqual(
            s, Student(
                "Galina", "Moskoviskaya",
                "female", date(1992, 4, 12), 161, 6
            )
        )


class TestGroup(unittest.TestCase):

    @staticmethod
    def _get_group():
        return [
            Student("a", "a", "a", date(1997, 1, 1), 1, 1),
            Student("a", "a", "a", date(1993, 1, 1), 1, 1),
            Student("a", "a", "a", date(1994, 1, 1), 1, 1)
        ]

    def test_encapsulation(self):

        self.assertTrue(not issubclass(Group, list))
        self.assertTrue(not issubclass(Group, Iterable))

    def test_str(self):
        group = self._get_group()
        exp_str = [f"Student({s})" for s in group]
        exp_str = f"Group({exp_str})"
        self.assertEqual(str(Group(group)), exp_str)

    def test_init(self):
        g = Group(self._get_group())
        a = Group(tuple(self._get_group()))
        self.assertEqual(a, g)

        def iterable(group):
            for s in group:
                yield s

        a = Group(iterable(self._get_group()))
        self.assertEqual(a, g)

    def test_sort_by_ages(self):
        s1 = Student("a", "a", "a", date(1997, 1, 1), 1, 1)
        s2 = Student("a", "a", "a", date(1993, 1, 1), 1, 1)
        s3 = Student("a", "a", "a", date(1994, 1, 1), 1, 1)
        g = Group([s1, s2, s3])

        g.sort_by_age()
        self.assertEqual(str(g), str(Group([s1, s3, s2])))
        g.sort_by_age(reverse=True)
        self.assertEqual(str(g), str(Group([s2, s3, s1])))

        s4 = Student("a", "a", "a", date(1992, 1, 1), 1, 1)

        for group in permutations([s1, s2, s3, s4]):

            g = Group(group)
            g.sort_by_age()
            self.assertEqual(str(g), str(Group([s1, s3, s2, s4])))
            g.sort_by_age(reverse=True)
            self.assertEqual(str(g), str(Group([s4, s2, s3, s1])))

    def test_sort_by_skill(self):
        s1 = Student("a", "a", "a", date(1997, 1, 1), 1, 1)
        s2 = Student("a", "a", "a", date(1993, 1, 1), 1, 5)
        s3 = Student("a", "a", "a", date(1994, 1, 1), 1, 3)
        g = Group([s1, s2, s3])

        g.sort_by_skill()
        self.assertEqual(str(g), str(Group([s1, s3, s2])))
        g.sort_by_skill(reverse=True)
        self.assertEqual(str(g), str(Group([s2, s3, s1])))

        s4 = Student("a", "a", "a", date(1992, 1, 1), 1, 2)

        for group in permutations([s1, s2, s3, s4]):

            g = Group(group)
            g.sort_by_skill()
            self.assertEqual(str(g), str(Group([s1, s4, s3, s2])))
            g.sort_by_skill(reverse=True)
            self.assertEqual(str(g), str(Group([s2, s3, s4, s1])))

    def test_sort_by_age_and_skill(self):
        s1 = Student("a", "a", "a", date(1993, 1, 1), 1, 4)
        s2 = Student("a", "a", "a", date(1993, 1, 1), 1, 2)
        s3 = Student("a", "a", "a", date(1994, 1, 1), 1, 3)
        g = Group([s1, s2, s3])

        g.sort_by_age_and_skill()
        self.assertEqual(str(g), str(Group([s3, s2, s1])))
        g.sort_by_age_and_skill(reverse=True)
        self.assertEqual(str(g), str(Group([s1, s2, s3])))

        s4 = Student("a", "a", "a", date(1994, 1, 1), 1, 7)

        for group in permutations([s1, s2, s3, s4]):

            g = Group(group)
            g.sort_by_age_and_skill()
            self.assertEqual(str(g), str(Group([s3, s4, s2, s1])))
            g.sort_by_age_and_skill(reverse=True)
            self.assertEqual(str(g), str(Group([s1, s2, s4, s3])))

    def test_eq(self):
        g = Group(self._get_group())
        self.assertEqual(g, g)

        a = Group(self._get_group() + self._get_group())
        self.assertEqual(a, g)  # were assertNotEqual -- bad test
        a = deepcopy(g)
        a.sort_by_skill()
        self.assertEqual(g, a)
        a.sort_by_age(reverse=True)
        self.assertEqual(g, a)
        a.sort_by_age_and_skill(reverse=True)
        self.assertEqual(g, a)


if __name__ == "__main__":
    unittest.main()