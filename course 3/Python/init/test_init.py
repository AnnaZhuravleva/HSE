import unittest

try:
    from sol_init import FieldInitializer
except (ModuleNotFoundError, ImportError):
    from init import FieldInitializer


class TestFieldInitializer(unittest.TestCase):
    def test_sanity(self):
        class C(metaclass=FieldInitializer):
            pass

        c = C(foo=1)
        self.assertEqual(c.foo, 1)

    def test_attributes_not_overriden(self):
        class C(metaclass=FieldInitializer):
            def __init__(self):
                self.foo = 0xff

        c = C(foo=1)
        self.assertEqual(c.foo, 0xff)

    def test_attributes_passed_to_init(self):
        class C(metaclass=FieldInitializer):
            def __init__(self, foo):
                self.a = foo + 1

        c = C(foo=1)
        self.assertEqual(c.foo, 1)
        self.assertEqual(c.a, 2)

    def test_subclass_initialization(self):
        class A(metaclass=FieldInitializer):
            pass

        class B(A):
            pass

        b = B(attr="key")
        self.assertEqual(b.attr, "key")

    def test_mixed_args(self):
        class A(metaclass=FieldInitializer):
            def __init__(self, a, b, c, d=1):
                self.a = 1
                self.b = b
                self.d = d + 1

        a = A(1, 2, 3, foo=4, d=5)
        self.assertEqual(a.a, 1)
        self.assertEqual(a.b, 2)
        with self.assertRaises(AttributeError):
            _ = a.c

        self.assertEqual(a.d, 6)
        self.assertEqual(a.foo, 4)


if __name__ == "__main__":
    unittest.main()
