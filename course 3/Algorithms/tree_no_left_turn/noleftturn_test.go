package noleftturn

import (
	"reflect"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	values := make([]int, 0)

	// Recursive traversal that always goes to the right
	var rightTraversal func(tree *Tree)
	rightTraversal = func(tree *Tree) {
		if tree == nil {
			return
		}
		values = append(values, tree.Value)
		rightTraversal(tree.Right)
	}

	// Construct a test tree
	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{3, nil, nil})
	tree.Right = &(Tree{15, nil, nil})
	tree.Right.Left = &(Tree{12, nil, nil})
	tree.Right.Right = &(Tree{20, nil, nil})

	newTree := NoLeftTurn(&tree)
	rightTraversal(newTree)

	expected := []int{3, 10, 12, 15, 20}

	if !reflect.DeepEqual(expected, values) {
		t.Fatalf("Invalid result")
	}
}
