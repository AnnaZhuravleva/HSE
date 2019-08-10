package array

import (
	"fmt"
	"testing"
)

func TestGet(t *testing.T) {
	h := New(0)
	for i := 0; i < 10; i++ {
		h.Push(Element(i * i))
	}

	v, err := h.Get(5)
	fmt.Println("Get()", v)
	if v != 25 && err != nil {
		t.Errorf("Get returned an invalid result %v %v", h.elems, v)
	}

	v, err = h.Get(10)
	if err == nil {
		t.Fatal("Get returned an invalid result")
	}
	fmt.Println("Get()", v)
}

func TestSet(t *testing.T) {
	h := New(3)
	h.Push(1)
	err := h.Set(0, 42)
	if err != nil {
		t.Error("Failed to set an array element by valid index")
	}
}

func TestPush(t *testing.T) {

	h := New(0)
	h.Push(213423)

	v, err := h.Get(h.Len() - 1)

	if err != nil || v != 213423 {
		t.Error("Push test failed")
	}

	h.Push(123411)
	v, err = h.Get(h.Len() - 1)

	if err != nil || v != 123411 {
		t.Error("Push test failed")
	}
}

func TestString(t *testing.T) {
	h := New(0)
	if h.String() != "[]" {
		t.Fatal("String() is invalid for an empty array, expected []")
	}

	for i := 0; i < 10; i++ {
		h.Push(Element(i * i))
	}

	result := h.String()
	expected := "[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]"

	if result != expected {
		t.Fatalf("String() returned an invalid array representation\nResult: %s\nExpected: %s", result, expected)
	}
}
