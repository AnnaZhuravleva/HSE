import unittest
import string
import random

try:
    from sol_diamond import A, B, C, D
except (ModuleNotFoundError, ImportError):
    from diamond import A, B, C, D


class TestDiamond(unittest.TestCase):

    @staticmethod
    def reset():
        A._init = 0
        B._init = 0
        C._init = 0
        D._init = 0

    @staticmethod
    def gen_dict():
        nota = string.ascii_letters[1:]

        def rint(): return random.randrange(len(nota))

        result = {}
        for _ in range(rint()):
            key = nota[rint()]
            result[key] = key
        return result

    def test_a(self):
        a = A(a=1)
        self.assertDictEqual(a.__dict__, {'a': 1})
        self.assertEqual(A._init, 1)

        self.reset()

    def test_b(self):
        b = B(1, 2, 3)
        self.assertDictEqual(b.__dict__, {'a': 3, 'b1': 1, 'b2': 2})
        self.assertEqual(B._init, 1)
        self.assertEqual(A._init, 1)

        self.reset()

    def test_c(self):
        c = C(10, 11, 12)
        self.assertDictEqual(c.__dict__,  {'a': 12, 'c1': 10, 'c2': 11})
        self.assertEqual(C._init, 1)
        self.assertEqual(A._init, 1)

        self.reset()

    def test_d(self):
        d = D(1, 2, 3, 4, 5, 6, 7)
        self.assertDictEqual(
            d.__dict__,
            {'a': 7, 'c1': 5, 'c2': 6, 'b1': 3, 'b2': 4, 'd1': 1, 'd2': 2}
        )
        self.assertEqual(B._init, 1)
        self.assertEqual(C._init, 1)
        self.assertEqual(A._init, 1)

        self.reset()

    def test_random_a(self):
        for i in range(10):
            exp = self.gen_dict()
            a = A(a=12, **exp)
            exp['a'] = 12
            self.assertDictEqual(a.__dict__, exp)
            self.assertEqual(A._init, i + 1)

        self.reset()

    def test_random_b(self):
        for i in range(10):
            exp = self.gen_dict()
            b = B(13, 17, 19, **exp)
            exp['a'] = 19
            exp['b1'] = 13
            exp['b2'] = 17
            self.assertDictEqual(b.__dict__, exp)
            self.assertEqual(B._init, i + 1)
            self.assertEqual(A._init, i + 1)

        self.reset()


    def test_random_c(self):
        for i in range(10):
            exp = self.gen_dict()
            c = C(-11, -12, 19, **exp)
            exp['a'] = 19
            exp['c1'] = -11
            exp['c2'] = -12
            self.assertDictEqual(c.__dict__, exp)
            self.assertEqual(C._init, i + 1)
            self.assertEqual(A._init, i + 1)

        self.reset()

    def test_random_d(self):
        for i in range(100):
            exp = self.gen_dict()
            d = D(1, 2, 3, 4, 5, 6, 7, **exp)
            exp.update(
                {
                    'a': 7, 'c1': 5, 'c2': 6, 'b1': 3, 'b2': 4, 'd1': 1,
                    'd2': 2
                }
            )
            self.assertDictEqual(d.__dict__, exp)
            self.assertEqual(A._init, i + 1)
            self.assertEqual(B._init, i + 1)
            self.assertEqual(C._init, i + 1)
            self.assertEqual(D._init, i + 1)

        self.reset()


if __name__ == "__main__":
    random.seed(a=1)
    unittest.main()
