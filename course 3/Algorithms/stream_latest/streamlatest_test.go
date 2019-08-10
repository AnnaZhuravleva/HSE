package streamlatest

import (
	"reflect"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	stream := New(3)

	if _, ok := stream.Latest(0); ok {
		t.Fatalf("`Latest` did not return an error for an empty stream")
	}

	stream.Push(1)
	stream.Push(2)

	if _, ok := stream.Latest(2); ok {
		t.Fatalf("`Latest(2)` did not return an error for a stream of length 2")
	}

	if _, ok := stream.Latest(5); ok {
		t.Fatalf("`Latest(5)` did not return an error for k=3")
	}

	stream.Push(3)
	stream.Push(4)

	if _, ok := stream.Latest(5); ok {
		t.Fatalf("`Latest(5)` did not return an error for k=3")
	}

	latest := make([]int, 0)
	for i := 0; i < 3; i++ {
		l, ok := stream.Latest(i)
		if !ok {
			t.Fatalf("`Latest` returned an error for a valid element")
		}
		latest = append(latest, l)
	}

	if !reflect.DeepEqual(latest, []int{4, 3, 2}) {
		t.Fatalf("invalid latest elements")
	}
}
