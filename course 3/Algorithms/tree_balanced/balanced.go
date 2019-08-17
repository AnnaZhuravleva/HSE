package balanced

import "sort"

// A Tree is a binary tree with integer values.
type Tree struct {
	Value int
	Left  *Tree
	Right *Tree
}

func New(elements []int) *Tree {
	sort.Ints(elements)
	if len(elements) > 0 {
		elements = Deduplicate(elements)
	}
	return Construct(elements, 0, len(elements)-1)
}

func Deduplicate(values []int) []int {
	var count int
	for i := 1; i < len(values); i++ {
		if values[count] == values[i] {
			continue
		}
		count++
		values[count] = values[i]
	}
	return values[:count+1]
}

func Construct(elements []int, start int, end int) *Tree {
	if start > end {
		return nil
	}
	middle := (start + end) / 2
	tree := &Tree{Value: elements[middle], Left: nil, Right: nil}
	tree.Left = Construct(elements, start, middle-1)
	tree.Right = Construct(elements, middle+1, end)
	return tree
}

// func CountingSort(values []int) {
// 	max, min, k := -2147483648, 2147483647, -1
// 	for _, v := range values {
// 		if v < min {
// 			min = v
// 		}
// 		if v > max {
// 			max = v
// 		}
// 	}
// 	if len(values) > 0 {
// 		k = max - min + 1
// 	}
// 	count, output := make([]int, k+1), make([]int, len(values))
// 	key := func(v int) int { return v - min }
// 	for _, v := range values {
// 		count[key(v)+1]++
// 	}
// 	for i := 1; i < k; i++ {
// 		count[i] += count[i-1]
// 	}
// 	for i := len(values) - 1; i >= 0; i-- {
// 		output[count[key(values[i])]] = values[i]
// 		count[key(values[i])]++
// 	}
// 	copy(values, output)
// }
