package noleftturn

// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

// NoLeftTurn transforms a binary search tree into an equivalent one that has no left subtrees.
// Returns a pointer to the new root.
func tmp(tree *Tree, node *Tree) *Tree {
	if tree.Right == nil {
		tree.Right = node
	} else {
		tree.Right = tmp(tree.Right, node)
	}
	return tree
}

func NoLeftTurn(tree *Tree) *Tree {
	var node *Tree
	if tree != nil {
		tree.Right = NoLeftTurn(tree.Right)
		if tree.Left != nil {
			tree.Left = NoLeftTurn(tree.Left)
			node = tree.Left
			tree.Left = nil
			tree = tmp(node, tree)
		}
	}
	return tree
}
