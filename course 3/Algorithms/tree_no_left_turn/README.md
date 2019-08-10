# No Left Turn

Implement a function that turns a valid **binary search tree** into an equivalent one (i.e. containing the same values) that has no left subtrees.

For example, this BST
```
        ____8___
       /        \
    __3         _12___
   /   \       /      \
  1     6     10      _14
 / \     \           /
0   2     7         13
```

should be transformed into
```
0
 \
  1
   \
    2
     \
      3
       \
        6
         \
          7
           \
            8
             \
              10
                \
                 12
                   \
                    13
                      \
                       14
```

* The transformation has to be done in-place, i.e. without allocating any new nodes.
* The function has to return a pointer to the root of the new tree.
