package queue

import (
	"math/rand"
	"testing"
)

func TestUnit__QueueOrder(t *testing.T) {
	q := New()

	r := rand.New(rand.NewSource(0xDEADBEEF))

	var (
		input  []uint32
		output []uint32
		i      uint32
		n      uint32 = 100
	)

	for i = 0; i < n; i++ {
		input = append(input, r.Uint32()%1000)
	}

	for i = 0; i < n; i++ {
		q.Push(input[i])
	}

	for i = 0; i < n; i++ {
		v, _ := q.Pop()
		output = append(output, v)
	}

	for i = 0; i < n; i++ {
		if output[i] != input[i] {
			t.Fatalf("Order of Pop()'d elements differ from the order they were Push()'d into the queue %v %v %v %v", output, input, output[i], input[i])
		}
	}
}

func TestUnit__PopEmpty(t *testing.T) {
	q := New()
	_, err := q.Pop()
	if err == nil {
		t.Fatal("Expected an error when calling Pop() on an empty queue")
	}
}

func TestUnit__PopSingle(t *testing.T) {
	q := New()
	q.Push(100)

	v, err := q.Pop()
	if err != nil || v != 100 {
		t.Fatal("Failed to Pop() on a queue with a single element")
	}
}

func TestUnit__MaxEmpty(t *testing.T) {
	q := New()
	_, err := q.Max()
	if err == nil {
		t.Fatal("Expected an error when calling Max() on an empty queue")
	}
}

func TestUnit__MaxSingle(t *testing.T) {
	q := New()
	q.Push(100)

	v, err := q.Max()
	if err != nil || v != 100 {
		t.Fatal("Failed to Max() on a queue with a single element")
	}
}
