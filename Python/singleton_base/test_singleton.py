import unittest
import random

try:
    from sol_singleton import Singleton
except (ModuleNotFoundError, ImportError):
    from singleton import Singleton


class TestSingleton(unittest.TestCase):

    def assert_singleton(self, lhs, rhs):
        self.assertEqual(lhs, rhs)
        self.assertTrue(lhs is rhs)
        self.assertEqual(id(lhs), id(rhs))

    def test_simple(self):
        lhs = Singleton()
        rhs = Singleton()

        self.assert_singleton(lhs, rhs)

    def test_hard(self):
        size = 100
        slist = [Singleton() for _ in range(size)]

        def rint(): return random.randrange(size)

        for lhs_idx, rhs_idx in [
            (rint(), rint()) for _ in range(size ** 2)
        ]:
            self.assert_singleton(slist[lhs_idx], slist[rhs_idx])


if __name__ == "__main__":
    random.seed(a=1234)
    unittest.main()
