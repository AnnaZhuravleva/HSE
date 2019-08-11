import unittest

try:
    from sol_storage import Storage, Transaction
except (ModuleNotFoundError, ImportError):
    from storage import Storage, Transaction


class TestStorage(unittest.TestCase):

    def test_context(self):
        s = Storage()

        self.assertIsInstance(s.edit(), Transaction)
        self.assertTrue(hasattr(s.edit(), "__exit__"))
        self.assertTrue(hasattr(s.edit(), "__enter__"))

        with s.edit() as tr:
            self.assertIsInstance(tr, Transaction)

        with self.assertRaises(ValueError):
            with s.edit() as tr:
                int("Transaction")

    def test_transaction(self):
        s = Storage()

        with s.edit() as se:
            se["a"] = "a"
            se["b"] = "b"

        self.assertDictEqual(s._data, {"a": "a", "b": "b"})

        with s.edit() as se:
            del se["b"]

        self.assertDictEqual(s._data, {"a": "a"})

        with self.assertRaises(KeyError):
            with s.edit() as se:
                del se["b"]

        with s.edit() as se:
            se["a"] = 1
            se["b"] = 2
            se["c"] = 3

        self.assertDictEqual(s._data, {"a": 1, "b": 2, "c": 3})

        with self.assertRaises(ZeroDivisionError):
            with s.edit() as se:
                se["a"] = "a"
                1/0
        self.assertDictEqual(s._data, {"a": 1, "b": 2, "c": 3})

        with self.assertRaises(ValueError):
            with s.edit() as se:
                se["a"] = "a"
                se["d"] = 11
                int("abcfd")

        self.assertDictEqual(s._data, {"a": 1, "b": 2, "c": 3})

        with s.edit() as se:
            se["a"] = []
            se["a"].append(1)
            se["a"].append(2)
            exp_id = id(se["a"])
            del se["b"]
            del se["c"]

        self.assertDictEqual(s._data, {"a": [1, 2]})

        with self.assertRaises(AttributeError):
            with s.edit() as se:
                se["a"] = [1, 2]
                se["a"].abcd

        self.assertDictEqual(s._data, {"a": [1, 2]})
        self.assertEqual(id(s["a"]), exp_id)


if __name__ == "__main__":
    unittest.main()
