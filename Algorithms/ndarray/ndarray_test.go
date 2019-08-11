package ndarray

import (
	"fmt"
	"strings"
	"testing"
)

type TestCase struct {
	axes []uint32
	nidx []uint32
	idx  uint32
}

func printSlice(arr []uint32) string {
	var b strings.Builder
	for i, e := range arr {
		fmt.Fprintf(&b, "%d", e)
		if i < (len(arr) - 1) {
			b.WriteString(", ")
		}
	}
	return b.String()
}

func TestUnit__Basic(t *testing.T) {

	matrix := New(3, 3)
	idx, err := matrix.Idx(1, 1)

	if err != nil {
		t.Error(err)
	}

	if idx != 4 {
		t.Errorf("Invalid result: New(3, 3, 3).Idx(1, 1, 1) == %v, expected 4", idx)
	}
}

func TestUnit__ValidIdx(t *testing.T) {

	cases := []TestCase{
		{[]uint32{64}, []uint32{0}, 0},
		{[]uint32{64}, []uint32{63}, 63},
		{[]uint32{2, 2}, []uint32{0, 0}, 0},
		{[]uint32{2, 2}, []uint32{1, 1}, 3},
		{[]uint32{3, 3, 3, 3}, []uint32{0, 0, 0, 0}, 0},
		{[]uint32{3, 3, 3, 3}, []uint32{2, 2, 2, 2}, 80},
	}

	for _, cs := range cases {
		idx, err := New(cs.axes...).Idx(cs.nidx...)
		if err != nil {
			t.Error(err)
		}

		if idx != cs.idx {
			t.Errorf("Invalid result: New(%v).Idx(%v) == %v, expected %v", printSlice(cs.axes), printSlice(cs.nidx), idx, cs.idx)
		}
	}
}

func TestUnit__InvalidIdx(t *testing.T) {

	cases := []TestCase{
		{[]uint32{64}, []uint32{0, 0}, 0},
		{[]uint32{64}, []uint32{65}, 0},
		{[]uint32{2, 2}, []uint32{0, 0, 1}, 0},
		{[]uint32{2, 2}, []uint32{1, 1, 3}, 0},
		{[]uint32{3, 3, 3, 3}, []uint32{0, 0}, 0},
		{[]uint32{3, 3, 3, 3}, []uint32{5, 2, 2, 2}, 0},
	}

	for _, cs := range cases {
		idx, err := New(cs.axes...).Idx(cs.nidx...)
		if err == nil {
			t.Errorf("Invalid result: New(%v).Idx(%v) == %v, expected an error", printSlice(cs.axes), printSlice(cs.nidx), idx)
		}
	}
}
