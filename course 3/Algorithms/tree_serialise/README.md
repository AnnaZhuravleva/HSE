# Tree Construction and Serialisation

Let an *array representation* (or *serialized format*) of a binary tree is an array of strings constructed with level-order traversal of the tree. Numbers denote node values, and `nil` denotes an absence of node.

For example, an array `["6", "5", "7", "2", "nil", "nil", "8"]` represents the following tree:
```
    __6
   /   \
  5     7
 /       \
2         8
```

The array representation is *normalised* in a sense that it does not contain trailing `nil`s. While technically `["6", "5", "7", "2", "nil", "nil", "8", "nil", "nil", "nil"]` denotes the same tree, we will always prefer representations without useless suffixes of `nil`s.

More examples can be found at https://leetcode.com/faq/#binary-tree (with a minor difference of using `null` instead of `nil`).

# Problem

Implement two functions:

* `New(data []string)`, which constructs a binary tree from the given array representation;
* `Serialise(tree *Tree)`, which returns a normalised array representation of the given tree.
