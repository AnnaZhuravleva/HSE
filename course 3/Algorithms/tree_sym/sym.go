package sym

//import "fmt"
// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

func IsSymTree(tree *Tree) bool {
	if tree == nil {
		return true
	}
	return Walker(tree.Left, tree.Right)
}

func Walker(left, right *Tree) bool {
	if left == nil && right == nil {
		return true
	} else if left == nil || right == nil {
		return false
	}
	return left.Value == right.Value && Walker(left.Left, right.Right) && Walker(left.Right, right.Left)
}
