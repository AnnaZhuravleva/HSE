import unittest

try:
    from sol_force_load import force_load
except (ModuleNotFoundError, ImportError):
    from force_load import force_load


class TestForceLoad(unittest.TestCase):

    def test_bar(self):
        module_dict = force_load("bad_bar")

        self.assertEqual(len(module_dict), 2)
        self.assertIn("bar", module_dict)

        bar = module_dict["bar"]

        self.assertTrue(callable(bar))
        self.assertEqual(bar(2), "barbar")
        self.assertEqual(bar(11), "bar" * 11)

        self.assertEqual(bar.__name__, "bar")
        self.assertEqual(bar.__doc__, "\n    :param n: int\n"
                                      "    :return: str, n times \"bar\"\n"
                                      "    ")

        self.assertIn("math", module_dict)

        with self.assertRaises(AssertionError):
            bar([])

        math = module_dict["math"]
        import math as math_exp

        self.assertIs(math, math_exp)

    def test_foo(self):
        module_dict = force_load("bad_foo")

        self.assertEqual(len(module_dict), 1)
        self.assertIn("foo", module_dict)

        foo = module_dict["foo"]

        self.assertTrue(callable(foo))
        self.assertEqual(foo(2), "2 foo")
        self.assertEqual(foo(11), "11 foo")
        self.assertEqual(foo.__name__, "foo")

    def test_foo_bar(self):
        module_dict = force_load("bad_foo_bar")

        self.assertEqual(len(module_dict), 2)
        self.assertIn("Foo", module_dict)
        self.assertIn("Bar", module_dict)

        Foo, Bar = module_dict["Foo"], module_dict["Bar"]

        self.assertEqual(str(Foo()), "Foo")
        self.assertEqual(str(Bar()), "Bar")

    def test_hard(self):
        module_dict = force_load("bad_hard")

        self.assertEqual(len(module_dict), 3)
        self.assertIn("x", module_dict)
        self.assertIn("y", module_dict)
        self.assertIn("hard", module_dict)

        y, x, hard = module_dict.values()

        self.assertIsInstance(x, int)
        self.assertIsInstance(y, list)
        self.assertTrue(callable(hard))

        self.assertEqual(x, 22)
        self.assertListEqual(y, [1, 2, 3])
        self.assertEqual(hard(11), 11)
        self.assertEqual(hard(33), 11)
        self.assertEqual(hard(-111), "hard")
        self.assertEqual(hard(-1), "hard")
        self.assertNotEqual(hard(0), "not hard")
        self.assertIs(hard(0), None)


if __name__ == "__main__":
    unittest.main()
