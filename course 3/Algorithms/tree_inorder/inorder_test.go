package inorder

import (
	"reflect"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{12, nil, nil})
	tree.Right = &(Tree{13, nil, nil})
	tree.Right.Left = &(Tree{14, nil, nil})
	tree.Right.Right = &(Tree{15, nil, nil})

	expected := []int{12, 10, 14, 13, 15}
	result := Inorder(&tree)

	if !reflect.DeepEqual(result, expected) {
		t.Fatalf("Invalid result")
	}
}
