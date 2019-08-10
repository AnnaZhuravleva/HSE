package tsort

import (
	"reflect"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	_, err := TSort([]string{"1", "2", "3"})
	if err == nil {
		t.Fatal("An error is expected for odd number of elements")
	}

	_, err = TSort([]string{"1", "2", "2", "3", "3", "1"})
	if err == nil {
		t.Fatalf("An error is expected for a cyclic graph")
	}

	result, err := TSort([]string{"4", "5", "3", "4", "2", "3", "1", "2"})
	if err != nil || !reflect.DeepEqual(result, []string{"1", "2", "3", "4", "5"}) {
		t.Errorf("Invalid topological sort %v", result)
	}
}
