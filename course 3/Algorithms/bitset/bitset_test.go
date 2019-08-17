package bitset

import (
	//	"fmt"
	"testing"
)

func TestUnit__SetUnsetCount(t *testing.T) {

	bs := New(2000)

	// Setting bits
	for i := 0; i < 2000; i++ {
		err := bs.Set(i, true)
		if err != nil {
			t.Fatalf("Failed to set a bit")
		}
		if isSet, err := bs.Test(i); err != nil || !isSet {
			t.Fatalf("Failed to test a previously set bit1")
		}
		if bs.Count() != (i + 1) {
			t.Fatalf("Invalid bit count")
		}
	}

	// Unsetting bits
	for i := 1999; i >= 0; i-- {
		bs.Set(i, false)
		if isSet, err := bs.Test(i); err != nil || isSet {
			t.Fatalf("Failed to test a previously unset bit2")
		}
		if bs.Count() != i {
			t.Fatalf("Invalid bit count")
		}
	}
}
