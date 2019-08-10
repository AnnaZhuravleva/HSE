# Ancestry in O(1)

Consider nodes `A` and `B` of a rooted tree. `B` is called a *proper descendant* of `A` if there is a unique simple path from `A` to `B` and also `A != B`.

Implement an `Ancestry` data structure that allows to determine if a certain tree node is a proper descendant of another in `O(1)`

* `New()` constructs an `Ancestry` instance from the given tree
* All trees are *binary* with integer nodes (although not necessarily search trees).
* `IsDescendant(a, b)` is true if `b` is a proper descendant of `b`.
* You should probably read about properties of depth-first search (CLRS 22.3) before doing this assignment.

```go
// Suppose that `T` represents the following tree:
//      10
//    /   \
//  12     13
//        /   \
//       14    15

ancestry := New(T)
ancestry.IsDescendant(10, 15)  // -> true
ancestry.IsDescendant(10, 10)  // -> false
ancestry.IsDescendant(12, 14)  // -> false
ancestry.IsDescendant(14, 10)  // -> false
```
