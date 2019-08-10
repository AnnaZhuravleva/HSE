package deduplicate

// Node represents an element of singly-linked list
type Node struct {
	Value uint32
	Next  *Node
}

// Deduplicate removes duplicates from a sorted singly-linked list starting with `node`
func Deduplicate(node *Node) {

	for node != nil {
		n := new(Node)
		if node.Next != nil {
			n = node.Next
			if node.Value != n.Value {
				node = node.Next
			} else {
				node.Next = n.Next
			}
		} else {
			return
		}
	}
	return
}
