package sym

import (
	"testing"
)

func TestUnit__Sym(t *testing.T) {

	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{23, nil, nil})
	tree.Right = &(Tree{23, nil, nil})
	tree.Left.Left = &(Tree{34, nil, nil})
	tree.Right.Right = &(Tree{34, nil, nil})

	if IsSymTree(&tree) == false {
		t.Fatal("IsSymTree(tree) == false for a symmetric tree")
	}
}

func TestUnit__NonSym(t *testing.T) {

	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{23, nil, nil})
	tree.Right = &(Tree{23, nil, nil})
	tree.Left.Left = &(Tree{34, nil, nil})

	if IsSymTree(&tree) == true {
		t.Fatal("IsSymTree(tree) == true for a non-symmetric tree")
	}
}
