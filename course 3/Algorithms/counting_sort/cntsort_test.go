package cntsort

import (
	"sort"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	cases := [][]int{
		[]int{},
		[]int{999},
		[]int{5, 34, 8893},
		[]int{836, 3, 731},
		[]int{9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
		[]int{9, 8, -7, 6, -5, 4, 3, -2, 1, 0},
		[]int{1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
	}

	for _, cs := range cases {
		sortedData := make([]int, len(cs))
		copy(sortedData, cs)
		sort.Ints(sortedData)

		testData := make([]int, len(cs))
		copy(testData, cs)
		CountingSort(testData)

		if len(sortedData) != len(testData) {
			t.Fatal("Length of sorted array does not match the input")
		}

		for i, v := range testData {
			if sortedData[i] != v {
				t.Fatalf("Sorting is invalid for %v", cs)
			}
		}
	}
}
