package tree

import (
	"testing"
)

type Case struct {
	coins    []int
	amount   int
	expected int
}

func TestUnit__Change(t *testing.T) {

	inputs := []Case{
		Case{[]int{}, 0, 0},
		Case{[]int{}, 42, -1},
		Case{[]int{1, 2, 5, 10, 50, 100}, 2348, 30},
		Case{[]int{69, 70, 11, 80, 85, 22, 87}, 44, 2},
		Case{[]int{38, 10, 11, 16, 25}, 83, 4},
		Case{[]int{33, 73, 15, 16, 51, 20, 94}, 100, 3},
	}

	for _, inp := range inputs {

		result := Change(inp.coins, inp.amount)

		if result != inp.expected {
			t.Fatalf("Incorrect result: Change(%v, %v) == %v, expected %v", inp.coins, inp.amount, result, inp.expected)
		}
	}
}
