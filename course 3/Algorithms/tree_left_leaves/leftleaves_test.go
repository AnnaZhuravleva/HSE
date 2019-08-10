package leftleaves

import (
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{12, nil, nil})
	tree.Right = &(Tree{13, nil, nil})
	tree.Right.Left = &(Tree{14, nil, nil})
	tree.Right.Right = &(Tree{15, nil, nil})

	expected := 26
	r := SumOfLeftLeaves(&tree)

	if r != expected {
		t.Fatalf("SumOfLeftLeaves(tree) == %v, expected %v", r, expected)
	}
}
