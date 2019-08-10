import unittest

try:
    from sol_cached import cached
except (ModuleNotFoundError, ImportError):
    from cached import cached


@cached
def add(x, y, z):
    return x + y + z


class TestCached(unittest.TestCase):

    def test_wraps(self):
        @cached
        def add(x, y):
            """Add"""
            return x + y

        self.assertEqual(add(1, 33), 34)
        self.assertEqual(add(-100, 33), -67)
        self.assertEqual(add.__name__, "add")
        self.assertEqual(add.__doc__, "Add")
        self.assertEqual(add.__module__, "__main__")

    def test_counter(self):
        class Counter:
            __count = 0

            @classmethod
            def reset(cls):
                cls.__count = 0

            @classmethod
            def get(cls):
                return cls.__count

            @staticmethod
            @cached
            def __call__(*args, **kwargs):
                Counter.__count += 1
                return True

        counter = Counter()
        Counter.reset()

        counter(1, 2)
        counter(1, 2)

        self.assertEqual(Counter.get(), 1)

        counter(1, 3)
        counter(1, 3)
        counter(1, 4)
        counter(1, 4)
        counter(1, 3)

        self.assertEqual(Counter.get(), 3)

        Counter.reset()
        counter(1, 2, a="a")
        counter(1, 2, b="c")
        counter(1, 3, a="a")
        counter(1, 2, a="a")

        self.assertEqual(Counter.get(), 3)

        Counter.reset()
        counter(1, 2, 3, a=1)
        counter(1, 3, 2, a=1, b=2)
        counter(1, 2, c=1)
        counter(1, 3, 2, b=2, a=1)
        counter(1, 2, 3, a=1)
        counter(1, 3, 2, a=1, b=2)
        counter(1, 3, 2, a=1, b=2)
        counter(1, 3, 2, a=1, b=2)

        self.assertEqual(Counter.get(), 3)

        Counter.reset()

        for i in range(1000):
            [Counter()(test=k) for k in "test"]

        self.assertEqual(Counter.get(), 3)

    def test_ackermann(self):
        counter = 0

        @cached
        def ackermann(m, n):
            """
            https://en.wikipedia.org/wiki/Ackermann_function
            """
            nonlocal counter
            counter += 1
            if m == 0:
                return n + 1
            elif m > 0 and n == 0:
                return ackermann(m - 1, 1)
            elif m > 0 and n > 0:
                return ackermann(m - 1, ackermann(m, n - 1))

        ackermann(1, 0)
        self.assertEqual(counter, 2)

        counter = 0
        ackermann(0, 1)
        self.assertEqual(counter, 0)

        counter = 0
        ackermann(2, 3)
        self.assertEqual(counter, 18)

        counter = 0
        ackermann(1, 3)
        self.assertEqual(counter, 0)

        counter = 0
        ackermann(1, 3)
        self.assertEqual(counter, 0)

        counter = 0
        ackermann(2, 4)
        self.assertEqual(counter, 5)

        counter = 0
        ackermann(2, 10)
        self.assertEqual(counter, 30)


if __name__ == "__main__":
    unittest.main()
