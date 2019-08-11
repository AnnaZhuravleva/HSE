package tree

import (
	"testing"
)

func TestUnit__New(t *testing.T) {

	tree, err := New([]string{"10", "84", "34", "nil", "3", "3"})
	if err != nil {
		t.Fatal(err)
	}

	if tree.Value != 10 || tree.Left.Value != 84 || tree.Right.Value != 34 || tree.Right.Left.Value != 3 {
		t.Fatal("Constructed tree is invalid")
	}
}

func TestUnit__Serialise(t *testing.T) {

	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{84, nil, nil})
	tree.Right = &(Tree{34, nil, nil})
	tree.Left.Right = &(Tree{3, nil, nil})
	tree.Right.Left = &(Tree{3, nil, nil})

	result := Serialise(&tree)
	expected := []string{"10", "84", "34", "nil", "3", "3"}

	n := len(expected)
	if len(result) > len(expected) {
		n = len(result)
	}

	for i := 0; i < n; i++ {
		if expected[i] != result[i] {
			t.Fatal("Serialised data is incorrect")
		}
	}
}
