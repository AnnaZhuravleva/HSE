import unittest

try:
    from sol_takes import takes
except (ModuleNotFoundError, ImportError):
    from takes import takes


@takes(int, str, float)
def foo(*args):
    return [i for i in args]


@takes(int, str, list, float, set)
def bar(*args):
    return [i for i in args]


class TestTakes(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(len(foo(1, "a", 2.0)), 3)
        self.assertTrue(isinstance(foo(1, "test", 1.0)[-1], float))
        self.assertEqual(foo(1, "abc", 2.0)[1], "abc")
        self.assertTrue(isinstance(foo(1, "test", 1.0)[0], int))
        self.assertEqual(foo(1, "abc", 2.0)[1], "abc")

    def test_bar(self):
        self.assertTrue(isinstance(bar(12), list))
        self.assertEqual(len(bar(1, "a", [])), 3)
        self.assertEqual(len(bar(1, "a", [], 1.0, set())), 5)
        self.assertEqual(len(bar(1, "a", [], 1.0, set(), 3.0, [], 7)), 8)
        self.assertEqual(len(bar(1, "a", [], 1.0, set(), *range(33))), 38)

    def test_exception(self):
        self.assertRaises(TypeError, foo, "a")
        self.assertRaises(TypeError, bar, 1, "a", [], 1.0, 19)

        with self.assertRaises(TypeError) as e:
            foo(1, "test", 22)
        self.assertEqual(
            e.exception.args[0],
            "int argument in position 2 is not float object"
        )

        with self.assertRaises(TypeError) as e:
            foo([], "test", 22)
        self.assertEqual(
            e.exception.args[0],
            "list argument in position 0 is not int object"
        )

        with self.assertRaises(TypeError) as e:
            foo(22, {}, 22)
        self.assertEqual(
            e.exception.args[0],
            "dict argument in position 1 is not str object"
        )

        with self.assertRaises(TypeError) as e:
            bar(1, "test", [], set())
        self.assertEqual(
            e.exception.args[0],
            "set argument in position 3 is not float object"
        )

        with self.assertRaises(TypeError) as e:
            bar(1, [], [], set())
        self.assertEqual(
            e.exception.args[0],
            "list argument in position 1 is not str object"
        )

        with self.assertRaises(TypeError) as e:
            bar(1, "test", [], 3, set(), "test")
        self.assertEqual(
            e.exception.args[0],
            "int argument in position 3 is not float object"
        )


if __name__ == "__main__":
    unittest.main()
