package balanced

import (
	"testing"
)

func maxDepth(tree *Tree) int {
	if tree == nil {
		return 0
	}

	lm := maxDepth(tree.Left)
	rm := maxDepth(tree.Right)

	if lm > rm {
		return 1 + lm
	}
	return 1 + rm
}

func TestUnit__Basic(t *testing.T) {

	tree := New([]int{1, 2, 3, 4, 5, 6, 7, 8})

	diff := maxDepth(tree.Left) - maxDepth(tree.Right)
	if diff < 0 {
		diff = -diff
	}
	if diff > 1 {
		t.Fatal("Tree is not balanced")
	}
}
