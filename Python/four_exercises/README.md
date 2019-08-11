## four-exercises (4 points)

- ### divisible

Write a function `divisible(begin, end)` which will find all such numbers which are divisible by 7 but are not a multiple of 5,
between `begin` and `end` (both included). The numbers obtained should be returned in a space-separated sequence on a single line.

**Input:** `5, 14`
**Output:** `'7 14'`
**Hints:** `range`

- ### register_count
Write a function `register_count(string)` that accepts a sentence and calculate the number of upper case letters and lower case letters.

**Input:** `Hello world!`
**Output:** `{'UPPER': 1, 'LOWER': 9}`
**Hints:** `str.upper()`, `str.lower()`

- ### pairwise_diff
Write a function  `pairwise_diff(first, second)` that computes the proportion of bases that differ between two DNA sequences of the same length. Both inputs are strings.

**Input:** `aBC`, `ABC`
**Output:** 0.33
**Hints:** `assert`

- ### run_robot
A robot moves in a plane starting from the original point (0,0). The robot can move toward UP, DOWN, LEFT and RIGHT with a given steps. The trace of robot movement is shown as the following:
```
UP 5
DOWN 3
LEFT 3
RIGHT 2
```
The numbers after the direction are steps. Please write a function to compute the distance from current position after a sequence of movement and original point. If the distance is a float, then just print the nearest integer.
To test your implementation use `$ python3 test_robot.py`

**Input:** (from console or file using redirect `<` operator)
```
UP 5
DOWN 3
LEFT 3
RIGHT 2
```
**Output:** `2`
**Hints:** `while True`, `input()`
