package leftleaves

// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

// SumOfLeftLeaves returns the sum of left leaves values for the given tree
func SumOfLeftLeaves(tree *Tree) int {
	if tree == nil {
		return 0
	}
	if tree.Left != nil && tree.Left.Left == nil && tree.Left.Right == nil {
		return tree.Left.Value + SumOfLeftLeaves(tree.Right)
	}
	return SumOfLeftLeaves(tree.Right) + SumOfLeftLeaves(tree.Left)
}
