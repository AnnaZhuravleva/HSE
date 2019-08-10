import unittest
from collections import Generator

try:
    sol = __import__("sol_chain")
    chain = getattr(sol, "chain")
except (ModuleNotFoundError, ImportError):
    from chain import chain


class TestChain(unittest.TestCase):

    def test_generator(self):

        self.assertTrue(
            isinstance(chain(1), Generator),
            "Not a generator"
        )

    def test_arg(self):
        self.assertEqual(list(chain(1)), [1])
        self.assertEqual(list(chain([1, 2, 3])), [1, 2, 3])
        self.assertEqual(list(chain("test")), list("test"))
        self.assertEqual(list(chain(range(10))), list(range(10)))

    def test_args(self):
        self.assertEqual(
            list(chain(1, 2, 3, 4)), [1, 2, 3, 4]
        )
        self.assertEqual(
            list(chain("test", 1, 2)), list("test") + [1, 2]
        )

        expected = [1, 2, 1, 2, 1, 2]
        self.assertEqual(
            list(chain([1, 2], 1, 2, [1, 2])),
            expected
        )
        self.assertEqual(
            list(chain(1, [2], [1, 2], 1, [2])),
            expected
        )
        self.assertEqual(
            list(chain(1, 2, [1, 2, 1], [2])),
            expected
        )
        self.assertEqual(
            list(chain("test", 1, 2, [1, 2, 1], [2])),
            list("test") + expected
        )

    def test_recursion(self):
        self.assertEqual(
            list(chain(["test"])),
            list("test")
        )
        self.assertEqual(
            list(chain([["test"]])),
            list("test")
        )
        self.assertEqual(
            list(chain([[[["test"]]]])),
            list("test")
        )
        self.assertEqual(
            list(chain([["test"]], "test")),
            list("testtest")
        )
        self.assertEqual(
            list(chain([["test"]], [1, 2], ["test"])),
            list("test") + [1, 2] + list("test")
        )
        self.assertEqual(
            list(chain([["test"]], [[1], 2], ["test"])),
            list("test") + [1, 2] + list("test")
        )
        self.assertEqual(
            list(chain([[["test"]], [[[1], 2]], ["test"]])),
            list("test") + [1, 2] + list("test")
        )
        self.assertEqual(
            list(chain([[[["test"]], [[[1], 2]]], ["test"]])),
            list("test") + [1, 2] + list("test")
        )
        self.assertEqual(
            [
                i for i in chain(
                    list(
                        zip(
                            range(1, 100, 2),
                            [([[i]]) for i in range(2, 100, 2)]
                        )
                    )
                )
            ],
            list(range(1, 99))
        )


if __name__ == "__main__":
    unittest.main()
