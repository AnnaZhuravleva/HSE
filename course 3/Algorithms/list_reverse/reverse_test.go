package reverse

import (
	"testing"
)

func listToSlice(node *Node) []int {
	output := make([]int, 0)

	for node != nil {
		output = append(output, node.Value)
		node = node.Next
	}

	return output
}

func sliceToList(slice []int) *Node {
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
	r := Reverse(lst)

	if r != nil {
		t.Fatal("`Reverse` of an empty list is not empty")
	}
}

func TestUnit__Reverse(t *testing.T) {

	input := []int{8, 3, 7, 1, 9, 10}
	lst := sliceToList(input)

	expected := []int{10, 9, 1, 7, 3, 8}

	r := Reverse(lst)
	result := listToSlice(r)

	if len(result) != len(expected) {
		t.Fatalf("Incorrect result: length of the result differ from the original list")
	}

	for i := range result {
		if expected[i] != result[i] {
			t.Fatalf("Incorrect result: Reverse(%v) == %v, expected %v", input, result, expected)
		}
	}
}
