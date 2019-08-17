package cycle

import (
	"testing"
)

func TestUnit__Empty(t *testing.T) {
	var lst *Node

	if HasCycle(lst) != false {
		t.Fatal("HasCycle detected cycle in an empty list")
	}
}

func TestUnit__Cycle(t *testing.T) {

	node := Node{1, nil}
	node.Next = &node

	if HasCycle(&node) == false {
		t.Fatal("HasCycle failed to detect a cycle")
	}

	node = Node{1, &Node{2, &Node{3, nil}}}
	node.Next.Next = node.Next

	if HasCycle(&node) == false {
		t.Fatal("HasCycle failed to detect a cycle")
	}

	node = Node{1, &Node{2, &Node{3, nil}}}

	if HasCycle(&node) == true {
		t.Fatal("HasCycle detected a cycle where there was no one")
	}
}
