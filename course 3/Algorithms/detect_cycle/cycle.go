package cycle

// Node represents an element of singly-linked list
type Node struct {
	Value int
	Next  *Node
}

// HasCycle detects whether the linked list has a cycle
func HasCycle(node *Node) bool {
	var slow, fast *Node
	slow = node
	fast = node
	for (slow != nil) && (fast != nil) && (fast.Next != nil) {
		slow = slow.Next
		fast = fast.Next.Next
		if slow == fast {
			return true
		}
	}
	return false
}
