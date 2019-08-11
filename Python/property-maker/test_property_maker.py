import unittest

try:
    from sol_property_maker import PropertyMaker
except (ModuleNotFoundError, ImportError):
    from property_maker import PropertyMaker


class TestPropertyMaker(unittest.TestCase):
    def test_simple(self):
        class A(metaclass=PropertyMaker):
            def __init__(self):
                self._secret_list = []
                self._a = None

            def get_a(self):
                self._secret_list.append("get")
                return self._a

            def set_a(self, value):
                self._secret_list.append("set")
                self._a = value

        obj = A()
        obj.a = 0xffffff
        self.assertEqual(obj.a, 0xffffff)
        self.assertEqual(obj._secret_list, ["set", "get"])
        for _ in range(5):
            obj.a = 111111
        self.assertEqual(obj._secret_list, ["set", "get"] + ["set"] * 5)

    def test_with_inheritance(self):
        class A(metaclass=PropertyMaker):
            pass

        class B(A):
            def __init__(self):
                self._secret_list = []

            def get_x(self):
                self._secret_list.append("get")
                return 0

            def set_x(self, value):
                self._secret_list.append("set")

        obj = B()
        obj.x = 4
        self.assertEqual(obj._secret_list, ["set"])
        _ = obj.x
        self.assertEqual(obj._secret_list, ["set", "get"])

    def test_partially_defined(self):
        class A(metaclass=PropertyMaker):
            def __init__(self):
                self._secret_list = []

            def get_x(self):
                self._secret_list.append("get")
                return 0

            def set_y(self, value):
                self._secret_list.append("set")
                self._y = value

        obj = A()
        _ = obj.x
        obj.y = 1

        self.assertEqual(obj._secret_list, ["get", "set"])

    def test_sanity(self):
        class Boo(metaclass=PropertyMaker):
            _boo = 0

            def get_raw_boo(self):
                return self._boo

            def get_boo(self):
                return self._boo % 42

            def set_boo(self, value):
                try:
                    self._boo = int(value)
                except ValueError:
                    raise TypeError("unproper value for boo: {}".format(value))

        boo = Boo()
        self.assertEqual(boo.raw_boo, 0)
        boo.boo = 43.5
        self.assertEqual(boo.raw_boo, 43)
        self.assertEqual(boo.boo, 1)
        with self.assertRaises(TypeError):
            boo.boo = "ggg"

    def test_multiple_usages(self):
        class A(metaclass=PropertyMaker):
            def get_x(self):
                return 0

        class B(metaclass=PropertyMaker):
            def get_x(self):
                return 1

        class C(metaclass=PropertyMaker):
            def set_x(self, value):
                self.value = value + 1

            def get_x(self):
                return self.value

        a = A()
        b = B()
        c = C()

        self.assertEqual(a.x, 0)
        self.assertEqual(b.x, 1)
        c.x = 5
        self.assertEqual(c.x, 6)


if __name__ == "__main__":
    unittest.main()
