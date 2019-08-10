import unittest

from vector import Vector


class TestVector(unittest.TestCase):

    def test_repr(self):
        v = Vector([1, 2, 3])

        self.assertEqual(str(v), "Vector([1, 2, 3])")
        self.assertEqual(repr(v), str(v))

        v = Vector([1.0, 2, 3.0])

        self.assertEqual(str(v), "Vector([1.0, 2, 3.0])")
        self.assertEqual(repr(v), str(v))


if __name__ == "__main__":
    unittest.main()
