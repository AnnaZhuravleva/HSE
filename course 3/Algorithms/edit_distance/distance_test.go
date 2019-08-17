package distance

import (
	"testing"
)

type Case struct {
	s1       string
	s2       string
	expected int
}

func TestUnit__Distance(t *testing.T) {

	inputs := []Case{
		Case{"", "aaaaa", 5},
		Case{"bbbbb", "", 5},
		Case{"aaa", "bb", 2},
		Case{"a", "a", 0},
		Case{"a", "b", 1},
		Case{"vintner", "writers", 5},
		Case{"923423235", "135312512352", 7},
		Case{"мошка", "мускат", 5},
	}

	for _, inp := range inputs {

		result := EditDistance(inp.s1, inp.s2)

		if result != inp.expected {
			t.Errorf("Incorrect result: EditDistance(\"%v\", \"%v\") == %v, expected %v", inp.s1, inp.s2, result, inp.expected)
		}
	}
}
