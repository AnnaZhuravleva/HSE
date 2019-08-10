package ancestry

import (
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	//      10
	//    /   \
	//  12     13
	//        /   \
	//       14    15

	tree := Tree{10, nil, nil}
	tree.Left = &(Tree{12, nil, nil})
	tree.Right = &(Tree{13, nil, nil})
	tree.Right.Left = &(Tree{14, nil, nil})
	tree.Right.Right = &(Tree{15, nil, nil})

	ancestry := New(&tree)

	if ancestry.IsDescendant(13, 13) != false { // not a **proper** descendant
		t.Fatal("Incorrect result")
	}

	if ancestry.IsDescendant(12, 15) != false {
		t.Fatal("Incorrect result")
	}

	if ancestry.IsDescendant(13, 14) != true {
		t.Fatal("Incorrect result")
	}

	if ancestry.IsDescendant(10, 15) != true {
		t.Fatal("Incorrect result")
	}
}
