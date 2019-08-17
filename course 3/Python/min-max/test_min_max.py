import unittest

try:
    from sol_min_max import minimum, maximum
except (ModuleNotFoundError, ImportError):
    from min_max import minimum, maximum


class Int:
    pass


class ComparableInt(int):
    num_calls = [0, 0]

    def __lt__(self, other):
        self.num_calls[0] += 1
        return super().__lt__(other)

    def __gt__(self, other):
        self.num_calls[1] += 1
        return super().__lt__(other)

    @classmethod
    def reset(cls):
        cls.num_calls = [0, 0]


class MinMaxTest(unittest.TestCase):

    def test_args(self):
        self.assertEqual(minimum(1, 2, 3), min(1, 2, 3))
        self.assertEqual(minimum([1], [2], [3]), min([1], [2], [3]))
        self.assertEqual(minimum('a', 'b', 'c'), min('a', 'b', 'c'))

        self.assertEqual(maximum(1, 2, 3), max(1, 2, 3))
        self.assertEqual(maximum([1], [2], [3]), max([1], [2], [3]))
        self.assertEqual(maximum('a', 'b', 'c'), max('a', 'b', 'c'))

    def test_iterable(self):

        def gen():
            yield from [1, 2, 3]

        self.assertEqual(minimum([1, 2, 3]), min([1, 2, 3]))
        self.assertEqual(minimum({1, 2, 3}), min({1, 2, 3}))
        self.assertEqual(minimum(range(10)), min(range(10)))
        self.assertEqual(minimum("test"), min("test"))
        self.assertEqual(
            minimum(map(lambda x: x ** 2, [-1, -2, -3])),
            min(map(lambda x: x ** 2, [-1, -2, -3]))
        )
        self.assertEqual(minimum(gen()), min(gen()))

        self.assertEqual(maximum([1, 2, 3]), max([1, 2, 3]))
        self.assertEqual(maximum({1, 2, 3}), max({1, 2, 3}))
        self.assertEqual(maximum(range(10)), max(range(10)))
        self.assertEqual(maximum("test"), max("test"))
        self.assertEqual(
            maximum(map(lambda x: x ** 2, [-1, -2, -3])),
            max(map(lambda x: x ** 2, [-1, -2, -3]))
        )
        self.assertEqual(maximum(gen()), max(gen()))

    def test_exceptions(self):
        with self.assertRaises(TypeError) as e:
            minimum(1, [1])
        with self.assertRaises(TypeError) as exp:
            min(1, [1])
        self.assertEqual(e.exception.args, exp.exception.args)

        with self.assertRaises(TypeError) as emin:
            minimum(Int())
        with self.assertRaises(TypeError) as emax:
            maximum(Int())
        with self.assertRaises(TypeError) as exp:
            min(Int())
        self.assertEqual(emin.exception.args, exp.exception.args)
        self.assertEqual(emax.exception.args, exp.exception.args)

        with self.assertRaises(TypeError) as emin:
            minimum(1)
        with self.assertRaises(TypeError) as emax:
            maximum(1)
        with self.assertRaises(TypeError) as exp:
            min(1)
        self.assertEqual(emin.exception.args, exp.exception.args)
        self.assertEqual(emax.exception.args, exp.exception.args)

        with self.assertRaises(TypeError) as e:
            maximum(1, [1])
        with self.assertRaises(TypeError) as exp:
            max(1, [1])
        self.assertEqual(e.exception.args, exp.exception.args)

    def test_key(self):
        self.assertEqual(
            minimum(["test", "a", "aba", "c"], key=len),
            min(["test", "a", "aba", "c"], key=len)
        )

        self.assertEqual(
            maximum(["test", "a", "aba", "c"], key=len),
            max(["test", "a", "aba", "c"], key=len)
        )

        self.assertEqual(
            minimum(range(100), key=lambda x: -x),
            maximum(range(100))
        )

        self.assertEqual(
            maximum(range(100), key=lambda x: -x),
            minimum(range(100))
        )

        d = {'a': 1, 'b': 2, 'c': 33, 'v': 13, 'd': -1}
        self.assertEqual(
            minimum(d, key=d.get),
            min(d, key=d.get)
        )

        self.assertEqual(
            maximum(d, key=d.get),
            max(d, key=d.get)
        )

    def test_cmp_operators(self):
        cmp_ints = [ComparableInt(i) for i in range(100)]

        minimum(cmp_ints)
        calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        min(cmp_ints)
        exp_calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        self.assertEqual(calls, exp_calls)

        maximum(cmp_ints)
        calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        max(cmp_ints)
        exp_calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        self.assertEqual(calls, exp_calls)

        cmp_ints = [ComparableInt(i) for i in (-1, 2, -3, 12, 17, -2, 90, -22)]

        minimum(cmp_ints)
        calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        min(cmp_ints)
        exp_calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        self.assertEqual(calls, exp_calls)

        maximum(cmp_ints)
        calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        max(cmp_ints)
        exp_calls = ComparableInt.num_calls.copy()
        ComparableInt.reset()

        self.assertEqual(calls, exp_calls)


if __name__ == "__main__":
    unittest.main()
