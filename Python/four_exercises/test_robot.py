import unittest
from unittest.mock import patch

import math
import random

from four_exercises import run_robot


class TestRobot(unittest.TestCase):

    @staticmethod
    def run_robot(user_input):
        with patch('builtins.input', side_effect=user_input):
            return run_robot()

    def test_one(self):
        user_input = [
            'UP 5',
            'DOWN 5',
            ''
        ]
        self.assertEqual(self.run_robot(user_input), 0)

    def test_two(self):
        user_input = [
            'UP 5',
            'DOWN 5',
            'LEFT 2',
            'RIGHT 3',
            'LEFT 1',
            ''
        ]
        self.assertEqual(self.run_robot(user_input), 0)

    def test_three(self):
        user_input = [
            'UP 5',
            'DOWN 5',
            'LEFT 2',
            'RIGHT 3',
            'LEFT 1',
            'RIGHT 2',
            'UP 1',
            ''
        ]
        self.assertEqual(self.run_robot(user_input), 2)

    def test_four(self):
        user_input = [
            'UP 22',
            'DOWN 5',
            'LEFT 8',
            'RIGHT 3',
            'LEFT 13',
            'RIGHT 2',
            'UP 1',
            ''
        ]
        self.assertEqual(self.run_robot(user_input), 24)



if __name__ == '__main__':
    random.seed(a=1)
    unittest.main()
