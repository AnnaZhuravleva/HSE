import unittest

try:
    from sol_semaphore import InstanceSemaphore, TooManyInstances
except (ModuleNotFoundError, ImportError):
    from semaphore import InstanceSemaphore, TooManyInstances


class TestInstanceSemaphore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class A(metaclass=InstanceSemaphore):
            __max_instance_count__ = 2

            def __init__(self):
                self.a = 1

            def get(self):
                return self.a

        class B(metaclass=InstanceSemaphore):

            __max_instance_count__ = 3

            def __init__(self):
                self.b = 2

            def get(self):
                return self.b

        self.A = A
        self.B = B

    def test_simple(self):
        a = self.A()
        b = self.B()
        self.assertEqual(a.get(), 1)
        self.assertEqual(b.get(), 2)

    def test_create(self):
        a = self.A()
        b = self.A()
        c = self.B()
        d = self.B()
        e = self.B()

    def test_fail_create_a(self):
        a = self.A()
        b = self.A()
        with self.assertRaises(TooManyInstances):
            self.A()

    def test_fail_create_b(self):
        a = self.B()
        b = self.B()
        c = self.B()
        with self.assertRaises(TooManyInstances):
            self.B()

    def test_del(self):
        a = self.A()
        a = self.A()
        a = self.A()
        a = self.A()
        a1 = self.A()
        with self.assertRaises(TooManyInstances):
            a2 = self.A()
        del a
        a2 = self.A()


if __name__ == "__main__":
    unittest.main()
