import unittest

from buckets import Buckets
from buckets_corrected import Buckets as Buckets_corrected


class MyTestCase(unittest.TestCase):

    @unittest.expectedFailure
    def test_incorrect_buckets(self):
        default = [1, 2, 3, 4]
        b = Buckets(5, default)

        default.append(5)
        self.assertTrue(b.find(4, [1, 2, 3, 4, 5]))

    def test_correct_buckets(self):
        default = [[1], [2]]
        bc = Buckets_corrected(5, default)

        self.assertNotEqual(id(default), id(bc.default))

        default[-1].append(3)
        self.assertTrue(bc.find(1, [2, 3]))

        default[-1].pop(-1)
        self.assertFalse(bc.find(4, 3))

        bc.add(3, 10)
        self.assertTrue(bc.find(3, 10))
        self.assertEqual(default,  [[1], [2]])

        bc.clear(3)
        self.assertFalse(bc.find(3, 10))

    def test_compare(self):
        default = [[1], [2], [3], 4, 5]
        b = Buckets(5, default)
        bc = Buckets_corrected(5, default)

        default[0].append(6)
        default.pop(4)

        self.assertTrue(b.buckets[0] == b.default == default)
        self.assertFalse(bc.buckets[0] == bc.default == default)


if __name__ == '__main__':
    unittest.main()
