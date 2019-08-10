import unittest

try:
    from sol_ocean import Ocean
except (ModuleNotFoundError, ImportError):
    from ocean import Ocean


class TestOcean(unittest.TestCase):

    @staticmethod
    def str_to_state(strin):
        return list(
            map(lambda x: list(map(int, x.split())), strin.split('\n'))
        )

    def test_str(self):
        state = "1 3\n" \
                "3 2"
        ocean = Ocean(init_state=self.str_to_state(state))
        self.assertEqual(str(ocean), state)

        state = "1 0 1\n" \
                "1 2 2\n" \
                "3 3 3\n" \
                "2 0 2"
        ocean = Ocean(init_state=self.str_to_state(state))
        self.assertEqual(str(ocean), state)

        state = "1 0 1 2 3 0 1\n" \
                "1 2 2 3 0 0 0"
        ocean = Ocean(init_state=self.str_to_state(state))
        self.assertEqual(str(ocean), state)

        state = "2 2 2 2\n" \
                "2 2 2 2\n" \
                "2 2 2 2\n" \
                "2 2 2 2"
        ocean = Ocean(init_state=self.str_to_state(state))
        self.assertEqual(str(ocean), state)

    def test_gen_next_quantum(self):
        state = "2 2 2 2\n" \
                "2 2 2 2\n" \
                "2 2 2 2\n" \
                "2 2 2 2"
        ocean = Ocean(init_state=self.str_to_state(state))

        expected = "2 0 0 2\n" \
                   "0 0 0 0\n" \
                   "0 0 0 0\n" \
                   "2 0 0 2"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        expected = "0 0 0 0\n" \
                   "0 0 0 0\n" \
                   "0 0 0 0\n" \
                   "0 0 0 0"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        state = "0 2 0 1 3\n" \
                "0 2 0 3 3\n" \
                "0 2 2 2 1\n" \
                "2 1 2 0 3\n" \
                "3 3 1 3 3"
        ocean = Ocean(init_state=self.str_to_state(state))

        expected = "0 0 0 1 3\n" \
                   "2 2 0 3 3\n" \
                   "2 0 0 2 1\n" \
                   "0 1 2 2 3\n" \
                   "0 0 1 3 3"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        for _ in range(100):
            self.assertEqual(str(ocean.gen_next_quantum()), expected)

        state = "0 2 0 1 3 3 3 3 3\n" \
                "0 2 0 3 3 3 3 3 3\n" \
                "0 2 2 2 1 3 3 3 3\n" \
                "2 1 2 0 3 2 2 2 2\n" \
                "3 3 1 3 3 2 2 2 2"
        ocean = Ocean(init_state=self.str_to_state(state))

        expected = "0 0 0 1 0 0 0 0 3\n" \
                   "2 2 0 3 0 0 0 0 0\n" \
                   "2 0 0 2 1 0 0 0 3\n" \
                   "0 1 2 2 3 2 0 0 2\n" \
                   "0 0 1 3 3 2 0 0 2"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        expected = "0 0 0 1 0 0 0 0 0\n" \
                   "2 2 0 0 0 0 0 0 0\n" \
                   "2 0 0 2 1 0 0 0 0\n" \
                   "0 1 2 2 3 0 0 0 0\n" \
                   "0 0 1 3 3 0 0 0 0"

        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        state = "0 2 1 0\n" \
                "0 2 1 0\n" \
                "0 2 1 0\n" \
                "0 2 1 0\n" \
                "0 2 1 0"
        ocean = Ocean(init_state=self.str_to_state(state))

        expected = "0 0 1 0\n" \
                   "2 2 1 0\n" \
                   "2 2 1 0\n" \
                   "2 2 1 0\n" \
                   "0 0 1 0"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        expected = "0 0 1 0\n" \
                   "2 2 1 0\n" \
                   "0 0 1 0\n" \
                   "2 2 1 0\n" \
                   "0 0 1 0"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        expected = "0 0 1 0\n" \
                   "0 0 1 0\n" \
                   "0 0 1 0\n" \
                   "0 0 1 0\n" \
                   "0 0 1 0"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        state = "3 2 3\n" \
                "1 0 2\n" \
                "3 2 1"
        ocean = Ocean(init_state=self.str_to_state(state))

        expected = "0 0 0\n" \
                   "1 2 2\n" \
                   "0 0 1"

        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        expected = "0 0 0\n" \
                   "1 0 0\n" \
                   "0 0 1"

        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        state = "3 2 3\n" \
                "1 3 2\n" \
                "3 1 1"
        ocean = Ocean(init_state=self.str_to_state(state))

        expected = "0 0 0\n" \
                   "1 3 0\n" \
                   "0 1 1"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)

        expected = "0 0 0\n" \
                   "1 0 0\n" \
                   "0 1 1"
        self.assertEqual(str(ocean.gen_next_quantum()), expected)


if __name__ == "__main__":
    unittest.main()
