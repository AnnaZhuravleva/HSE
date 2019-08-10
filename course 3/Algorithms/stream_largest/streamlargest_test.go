package streamlargest

import (
	"reflect"
	"sort"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	stream, _ := New(4)
	stream.Push(3)
	stream.Push(4)

	result := stream.Largest()
	sort.Ints(result)

	if !reflect.DeepEqual(result, []int{3, 4}) {
		t.Fatalf("invalid largest elements")
	}

	input := []int{64, 90, 65, 92, 33, 5, 30, 22, 23, 2, 85, 71, 66, 52, 73, 37, 59, 5, 27, 66}
	for _, v := range input {
		stream.Push(v)
	}

	result = stream.Largest()
	sort.Ints(result)

	if !reflect.DeepEqual(result, []int{73, 85, 90, 92}) {
		t.Fatalf("invalid largest elements %v", result)
	}

	stream.Push(100)
	stream.Push(300)
	stream.Push(200)

	result = stream.Largest()
	sort.Ints(result)

	if !reflect.DeepEqual(result, []int{92, 100, 200, 300}) {
		t.Fatalf("invalid largest elements %v", result)
	}
}
