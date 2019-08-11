package deduplicate

import (
	"testing"
)

func listToSlice(node *Node) []uint32 {
	output := make([]uint32, 0)

	for node != nil {
		output = append(output, node.Value)
		node = node.Next
	}

	return output
}

func sliceToList(slice []uint32) *Node {
	var start *Node
	node := start

	for _, c := range slice {
		n := new(Node)
		n.Value = c
		if start == nil {
			start = n
			node = n
		} else {
			node.Next = n
			node = n
		}
	}
	return start
}

func TestUnit__Empty(t *testing.T) {
	var lst *Node
	Deduplicate(lst)

	if lst != nil {
		t.Fatal("Deduplicate inserted something to an empty list")
	}
}

func TestUnit__Dedup(t *testing.T) {

	input := []uint32{1, 10, 10, 10, 10, 20, 30, 30, 50, 50, 100, 100, 100}
	lst := sliceToList(input)

	expected := []uint32{1, 10, 20, 30, 50, 100}

	Deduplicate(lst)
	result := listToSlice(lst)

	for i := range result {
		if expected[i] != result[i] {
			t.Fatalf("Incorrect result: Deduplicate(%v) == %v, expected %v", input, result, expected)
		}
	}
}
