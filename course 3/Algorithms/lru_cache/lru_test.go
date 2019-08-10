package lru

import (
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	cache := New(3)

	if cache.Get(1) != -1 {
		t.Fatal("Got something from an empty cache")
	}

	cache.Put(1, 1)
	if cache.Get(1) != 1 {
		t.Fatal("Could not read from cache")
	}

	cache.Put(2, 2)
	cache.Put(3, 3)
	if cache.Get(1) != 1 || cache.Get(2) != 2 || cache.Get(3) != 3 {
		t.Fatal("Could not read from cache")
	}

	cache.Get(1)
	cache.Put(4, 4)
	if cache.Get(1) == -1 {
		t.Fatal("The key was not expected to be removed")
	}
}
