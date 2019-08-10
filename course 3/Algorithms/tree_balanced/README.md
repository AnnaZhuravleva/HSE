# Constructing a Balanced BST

Implement a function that constructs a balanced binary search tree from the given array in `O(n lg n)` time.

The tree must contain unique elements even if the input array has duplicates.

```go
tree := New([]int{0, 1, -9, 1, 7, -10, 8, -2, 6, -1, 8})

// Possible result:
//
//          ___ 0 __
//         /        \
//      -2            7
//      / \         /   \
//    -9  -1       6     8
//    /           /
//  -10          1
```
