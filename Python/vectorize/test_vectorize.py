import unittest
import numpy

try:
    from sol_vectorize import Vector, Vectorize
except (ModuleNotFoundError, ImportError):
    from vectorize import Vector, Vectorize


class TestVectorize(unittest.TestCase):

    def test_one(self):
        @Vectorize
        def one(x):
            return x ** 3

        @numpy.vectorize
        def npone(x):
            return x ** 3

        self.assertTrue(
            isinstance(one([1, 2]), Vector)
        )
        self.assertEqual(
            str(one([1, 2, 3, 4, 5])),
            "Vector([1, 8, 27, 64, 125])"
        )
        self.assertEqual(
            one([-1, -2, 3, 4, 5]),
            Vector(npone([-1, -2, 3, 4, 5]))
        )
        self.assertEqual(
            one(list(range(200))),
            Vector(npone(list(range(200))))
        )

   # @unittest.skip("bonus, 2 points")
    def test_kwtwo(self):
        @Vectorize
        def kwtwo(x, y=22):
            return x ** 2 + y

        @numpy.vectorize
        def npkwtwo(x, y=22):
            return x ** 2 + y

        self.assertEqual(
            kwtwo([1, 10]),
            Vector(npkwtwo([1, 10]))
        )
        self.assertEqual(
            kwtwo([1, 10, 20, 30, 40]),
            Vector(npkwtwo([1, 10, 20, 30, 40]))
        )
        self.assertEqual(
            kwtwo([1, 10], [4]),
            Vector(npkwtwo([1, 10], [4]))
        )
        self.assertEqual(
            kwtwo([1, 10], 4),
            Vector(npkwtwo([1, 10], 4))
        )
        self.assertEqual(
            kwtwo([1, 10], 14),
            Vector(npkwtwo([1, 10], 14))
        )

    def test_three(self):
        @Vectorize
        def three(x, y, z):
            return x ** 2 + y ** 2 + z

        @numpy.vectorize
        def npthree(x, y, z):
            return x ** 2 + y ** 2 + z

        self.assertTrue(
            isinstance(three([1, 1, 1], [0, 0, 0], [1, 2, 3]), Vector)
        )
        self.assertEqual(
            str(three([1, 2], [2, -2], [1, -32])),
            "Vector([6, -24])"
        )
        self.assertEqual(
            str(three([1, 2, 3], [2, 44, 4], [1, 2, 3])),
            "Vector([6, 1942, 28])"
        )
        self.assertEqual(
            three([6, 7, 22], [22, 44, 43], [11, 27, 322]),
            Vector(npthree([6, 7, 22], [22, 44, 43], [11, 27, 322]))
        )

        self.assertEqual(
            three([6, 7, 22, 1], [22, 44, 43, 3], [11, 27, 322, 44]),
            Vector(npthree([6, 7, 22, 1], [22, 44, 43, 3], [11, 27, 322, 44]))
        )


if __name__ == "__main__":
    unittest.main()
