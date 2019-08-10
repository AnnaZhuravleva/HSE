package tree

import (
	"errors"
	// "fmt"
	"strconv"
)

// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

// New creates a binary tree from the array representation
func New(data []string) (*Tree, error) {
	return buildTree(data, nil, 0)
}

func buildTree(data []string, root *Tree, idx int) (*Tree, error) {
	if idx < len(data) {
		tmp := 2*idx + 1
		i, ok := strconv.Atoi(data[idx])
		if ok != nil {
			if data[idx] != "nil" {
				return nil, errors.New("error")
			}
			if (tmp < len(data) || tmp+1 < len(data)) && data[tmp] != "nil" {
				return nil, errors.New("error")
			}
			return nil, nil
		}
		root = &Tree{i, nil, nil}
		var err0, err1 error
		root.Left, err0 = buildTree(data, root.Left, tmp)
		root.Right, err1 = buildTree(data, root.Right, tmp+1)
		if err0 != nil || err1 != nil {
			return nil, errors.New("error")
		}
	}
	return root, nil
}

// Serialise returns a normalised array representation of the given tree
func Serialise(tree *Tree) []string {
	result := make([]string, 0)
	queue := []*Tree{tree}
	var nodes int
	if tree != nil {
		nodes = 1
	}
	for len(queue) > 0 && nodes > 0 {
		tmp := queue[0]
		queue = queue[1:]
		if tmp == nil {
			result, queue = append(result, "nil"), append(queue, nil, nil)
		} else {
			result, queue = append(result, strconv.Itoa(tmp.Value)), append(queue, tmp.Left, tmp.Right)
			nodes--
			if tmp.Left != nil {
				nodes++
			}
			if tmp.Right != nil {
				nodes++
			}
		}
	}
	return result
}
