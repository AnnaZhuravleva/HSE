import unittest

try:
    from sol_wraps import wraps, foo, decorator
except (ModuleNotFoundError, ImportError):
    from wraps import wraps, foo, decorator


@decorator
def bar(x):
    """Docstring bar"""
    return x


class TestWraps(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(foo.__name__, "foo")
        self.assertEqual(foo.__doc__, "Docstring foo")
        self.assertEqual(foo.__module__, wraps.__module__)

    def test_bar(self):
        self.assertEqual(bar.__name__, "bar")
        self.assertEqual(bar.__doc__, "Docstring bar")
        self.assertEqual(bar.__module__, "__main__")


if __name__ == "__main__":
    unittest.main()
