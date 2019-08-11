package ancestry

// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

// Ancestry allows to determine if a certain tree node is a proper descendant of another in O(1)
type Ancestry struct {
	m map[int]map[int]bool
}

func DFS(tmp *Ancestry, tree *Tree) map[int]bool {
	tmp.m[tree.Value] = make(map[int]bool)
	if tree != nil {
		if tree.Right != nil {
			tmp.m[tree.Value][tree.Right.Value] = true
			for k, v := range DFS(tmp, tree.Right) {
				tmp.m[tree.Value][k] = v
			}
		}
		if tree.Left != nil {
			tmp.m[tree.Value][tree.Left.Value] = true
			for k, v := range DFS(tmp, tree.Left) {
				tmp.m[tree.Value][k] = v
			}
		}
		return tmp.m[tree.Value]
	} else {
		return nil
	}
}

// New creates an instance of `Ancestry` from a binary tree with unique integer nodes
func New(tree *Tree) *Ancestry {
	tmp := new(Ancestry)
	tmp.m = make(map[int]map[int]bool)
	tmp.m[tree.Value] = make(map[int]bool)
	if tree != nil {
		if tree.Right != nil {
			tmp.m[tree.Value][tree.Right.Value] = true
			for k, v := range DFS(tmp, tree.Right) {
				tmp.m[tree.Value][k] = v
			}
		}
		if tree.Left != nil {
			tmp.m[tree.Value][tree.Left.Value] = true
			for k, v := range DFS(tmp, tree.Left) {
				tmp.m[tree.Value][k] = v
			}
		}
	}
	return tmp
}

// IsDescendant determines if node `b` is a proper descendant of `a` in O(1)
func (anc *Ancestry) IsDescendant(a, b int) bool {
	return anc.m[a][b]
}