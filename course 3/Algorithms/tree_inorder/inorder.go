package inorder

// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

// Inorder returns an inorder traversal of the given tree
func Inorder(tree *Tree) []int {
	inorder := make([]int, 0)
	tmp := make([]*Tree, 0)
	for tree != nil || len(tmp) > 0 {
		for tree != nil {
			tmp = append(tmp, tree)
			tree = tree.Left
		}
		inorder = append(inorder, tmp[len(tmp)-1].Value)
		tree = tmp[len(tmp)-1].Right
		tmp = tmp[:len(tmp)-1]
	}
	return inorder
}
