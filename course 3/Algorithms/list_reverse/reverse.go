package reverse

// Node represents an element of singly-linked list
type Node struct {
	Value int
	Next  *Node
}

// Reverse flips the original order of elements in the singly-linked list and returns a pointer to the resulting list
func Reverse(node *Node) *Node {
	if node == nil || node.Next == nil {
		return node
	}
	needle := node
	var t *Node = nil
	for {
		if needle == nil {
			break
		}
		f := needle.Next
		needle.Next = t
		t = needle
		needle = f
	}
	return t
}
