## buckets (2 points)


You are given the implementation of the class `Buckets` (see the file `buckets.py` and the description below). It contains one or more errors. Write detailed
Unit-tests using `unittest` module for this class to identify this error or errors. Explain, in
than the problem and write the correct version of this class. Correct version place in a file
`buckets_corrected.py`, tests - `test_buckets.py`. Specify which tests are not
passed by the primary implementation.

Description: class `Buckets` implements a set of containers in which
you can independently add items. When creating a class you can initialize
the number of containers and their initial states that can be
be non-empty. Further in the baskets you can put the items, check
presence of a specific item in the basket and clean them (return to
initial state). When you add items into the buckets,
it's not necessary to copy items (that is, the items can be changed from outside the class,
and their state must be changed inside class too).

**Hints:** `copy?`