import unittest
import abc

try:
    from sol_logger_mixin import LoggerMixin
except (ModuleNotFoundError, ImportError):
    from logger_mixin import LoggerMixin


class TestLoggerMixin(unittest.TestCase):

    def test_repeater(self):

        class Repeater(LoggerMixin):
            @staticmethod
            def repeat_a(n):
                return n * "a"

        r = Repeater()
        r.repeat_a(2)
        self.assertEqual(
            str(r),
            "Called repeat_a(). args: (2,), kwargs: {}, return: aa"
        )
        r.repeat_a(3)
        self.assertEqual(
            str(r),
            "Called repeat_a(). args: (2,), kwargs: {}, return: aa\n"
            "Called repeat_a(). args: (3,), kwargs: {}, return: aaa"
        )
        r.x = 1
        r.x
        Repeater.y = 11
        r.y
        Repeater.y
        r.repeat_a(4)
        self.assertEqual(
            str(r),
            "Called repeat_a(). args: (2,), kwargs: {}, return: aa\n"
            "Called repeat_a(). args: (3,), kwargs: {}, return: aaa\n"
            "Called repeat_a(). args: (4,), kwargs: {}, return: aaaa"
        )
        Repeater.repeat_a(1)
        self.assertEqual(
            str(r),
            "Called repeat_a(). args: (2,), kwargs: {}, return: aa\n"
            "Called repeat_a(). args: (3,), kwargs: {}, return: aaa\n"
            "Called repeat_a(). args: (4,), kwargs: {}, return: aaaa"
        )

    @unittest.skip("skip")
    def test_adder(self):
        class Arithmetic(abc.ABC):
            def __init__(self, value):
                self.value = value

            @abc.abstractmethod
            def add(self, *args, **kwargs):
                raise NotImplementedError

        class Adder(LoggerMixin, Arithmetic):

            def __init__(self, value):
                super().__init__()
                super(LoggerMixin, self).__init__(value)

            def add(self, a, b=None):
                if b:
                    return a + b
                else:
                    return self.value + a

        adder = Adder(100)
        adder.add(12)
        adder.add(10, b=11)
        adder.add(3, b=0)

        self.assertEqual(
            str(adder),
            "Called add(). args: (12,), kwargs: {}, return: 112\n"
            "Called add(). args: (10,), kwargs: {'b': 11}, return: 21\n"
            "Called add(). args: (3,), kwargs: {'b': 0}, return: 103"
        )

        adder.add(3, b=1222)
        adder.value = 11
        adder.value
        adder.add(4, b=-100)

        self.assertEqual(
            str(adder),
            "Called add(). args: (12,), kwargs: {}, return: 112\n"
            "Called add(). args: (10,), kwargs: {'b': 11}, return: 21\n"
            "Called add(). args: (3,), kwargs: {'b': 0}, return: 103\n"
            "Called add(). args: (3,), kwargs: {'b': 1222}, return: 1225\n"
            "Called add(). args: (4,), kwargs: {'b': -100}, return: -96"
        )


if __name__ == "__main__":
    unittest.main()
