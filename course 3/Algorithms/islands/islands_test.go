package islands

import (
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	if CountIslands([][]uint8{}) != 0 {
		t.Fatal("Incorrect result")
	}

	n := CountIslands(
		[][]uint8{
			[]uint8{0, 0, 1},
			[]uint8{0, 0, 1},
			[]uint8{0, 1, 0},
		},
	)
	if n != 2 {
		t.Fatal("Incorrect result")
	}

	n = CountIslands(
		[][]uint8{
			[]uint8{1, 0, 1},
			[]uint8{0, 1, 0},
			[]uint8{1, 0, 1},
		},
	)
	if n != 5 {
		t.Fatal("Incorrect result")
	}

}
