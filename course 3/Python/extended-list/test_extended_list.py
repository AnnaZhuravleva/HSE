import unittest
import random

try:
    from sol_extended_list import ExtendedList
except (ModuleNotFoundError, ImportError):
    from extended_list import ExtendedList


class TestExtendedList(unittest.TestCase):

    @classmethod
    def _get_index(cls, length):
        return random.randint(0, length - 1)

    @classmethod
    def _get_operator(cls):
        return random.choice(
            ["delitem", "setitem", "append", "insert", "first", "last", "size"]
        )

    @classmethod
    def _apply_operator(cls, el):
        op = cls._get_operator()
        index = cls._get_index(len(el))
        if op == "delitem":
            if len(el) > 1:
                del el[index]
        elif op == "setitem":
            el[index] = index
        elif op == "append":
            el.append(len(el) + 1)
        elif op == "insert":
            el.insert(index, len(el) + 1)
        elif op == "size":
            el.size = index if index != 0 else len(el) + 1
        elif op == "last":
            el.last = index
        elif op == "first":
            el.first = index

    def test_list(self):
        self.assertTrue(issubclass(ExtendedList, list))

    def test_property(self):
        with open(ExtendedList.__module__ + ".py", 'r') as f:
            for line in f.readlines():
                self.assertNotIn("property", line, "Do not use property!")

    def test_last(self):
        el = ExtendedList([1, 2, 3])

        self.assertEqual(el.L, 3)
        el.append(4)
        self.assertEqual(el.L, 4)
        el.append(5)
        el.append(6)
        self.assertEqual(el.L, 6)
        self.assertEqual(el.L, el.last)

        el = ExtendedList(range(4, -11, -2))
        self.assertEqual(el.L, -10)
        self.assertEqual(el.last, -10)
        del el[-1]
        self.assertEqual(el.last, -8)
        del el[-1]
        self.assertEqual(el.last, -6)
        self.assertEqual(el.L, -6)

        el.L = 11
        self.assertEqual(el.L, 11)
        self.assertEqual(el.last, el.L)
        self.assertEqual(el[-1], 11)
        el.last = "a"
        self.assertEqual(el.L, "a")
        self.assertEqual(el.last, el.L)
        self.assertEqual(el[-1], "a")

    def test_first(self):
        el = ExtendedList([1, 2, 3])

        self.assertEqual(el.F, 1)
        el[0] = 100
        self.assertEqual(el.F, 100)
        el[0] = -1
        self.assertEqual(el.first, -1)
        self.assertEqual(el.F, el.first)

        el = ExtendedList(range(4, -11, -2))
        self.assertEqual(el.F, 4)
        self.assertEqual(el.first, 4)
        del el[0]
        self.assertEqual(el.F, 2)
        del el[0]
        self.assertEqual(el.first, 0)
        self.assertEqual(el.F, 0)

        el.F = 11
        self.assertEqual(el.F, 11)
        self.assertEqual(el.first, el.F)
        self.assertEqual(el[0], 11)
        el.first = "a"
        self.assertEqual(el.F, "a")
        self.assertEqual(el.first, el.F)
        self.assertEqual(el[0], "a")

    def test_size(self):
        el = ExtendedList([1, 2, 3])

        self.assertEqual(el.S, 3)
        el.append(4)
        self.assertEqual(el.size, 4)
        el.append(5)
        el.append(6)
        self.assertEqual(el.S, 6)
        self.assertEqual(el.size, el.S)

        el = ExtendedList(range(4, -11, -2))
        self.assertEqual(el.S, 8)
        self.assertEqual(el.size, 8)
        del el[2]
        self.assertEqual(el.size, 7)
        del el[1]
        del el[3]
        self.assertEqual(el.size, 5)
        el.S = 11
        self.assertEqual(
            el,
            [4, -2, -4, -8, -10] + 6 * [None]
        )
        el.S = 9
        self.assertEqual(
            el,
            [4, -2, -4, -8, -10] + 4 * [None]
        )
        el.S = 3
        self.assertEqual(el, [4, -2, -4])
        el.S = 4
        self.assertEqual(el, [4, -2, -4, None])
        el.S = 0
        self.assertFalse(el)

    def test_reversed(self):
        el = ExtendedList([1, 2, 3])

        self.assertEqual(el.R, [3, 2, 1])
        el.append(4)
        self.assertEqual(el.reversed, [4, 3, 2, 1])
        el.append(5)
        el.append(6)
        self.assertEqual(el.R, [6, 5, 4, 3, 2, 1])
        self.assertEqual(el.reversed, el.R)

        el = ExtendedList(range(4, -11, -2))
        self.assertEqual(el.R, list(reversed(el)))
        self.assertEqual(el.reversed, list(reversed(el)))
        del el[2]
        self.assertEqual(el.R, list(reversed(el)))
        del el[1]
        del el[3]
        self.assertEqual(el.R, list(reversed(el)))
        self.assertEqual(el.reversed, el.R)

    def test_all_random(self):
        el = ExtendedList(list(range(9999)))
        random.shuffle(el)

        for _ in range(9999):
            self._apply_operator(el)

            self.assertEqual(el.R, list(reversed(el)))
            self.assertEqual(el.R, el.reversed)

            self.assertEqual(el.S, len(el))
            self.assertEqual(el.size, len(el))

            self.assertEqual(el.L, el[-1])
            self.assertEqual(el.last, el[-1])

            self.assertEqual(el.F, el[0])
            self.assertEqual(el.first, el[0])

    def test_raises(self):
        empty = ExtendedList([])

        with self.assertRaises(IndexError):
            e = empty.L
        with self.assertRaises(IndexError):
            e = empty.F
        with self.assertRaises(IndexError):
            e = empty.last
        with self.assertRaises(IndexError):
            e = empty.first


if __name__ == "__main__":
    random.seed(a=123)
    unittest.main()
