package array

import (
	"errors"
	"strconv"
)

// Element is a type of an array element
type Element uint64

// Array is an implementation of list using expandable array
// with fast insertion to and deletion from the end
type Array struct {
	elems []Element
	n     int
	cap   int
}

// New creates a new Array with a given capacity
func New(cap int) *Array {
	return &Array{make([]Element, cap), 0, cap}
}

// Len returns the lenght of the array
func (a *Array) Len() int {
	return a.n
}

// Get retrieves an array element by index
func (a *Array) Get(i int) (Element, error) {
	if i >= 0 && i < a.n {
		return a.elems[i], nil
	}
	return 0, errors.New("index out of range")
}

// Set writes an element to array by index
func (a *Array) Set(i int, x Element) error {
	if i < a.cap && a.cap > 0 && i >= 0 && i < a.n {
		a.elems[i] = x
		return nil
	}
	return errors.New("out of range")
}

// Insert adds an element to thearray by index
func (a *Array) Insert(i int, x Element) error {
	if i < a.cap && a.cap > 0 && a.cap > a.n && i >= 0 && i < a.n {
		for e := a.cap - 1; e > i; e-- {
			v := a.elems[e-1]
			a.elems[e] = v
		}
		a.elems[i], a.n = x, a.n+1
		return nil
	} else if i < a.cap && a.cap > 0 && a.cap == a.n && i >= 0 && i < a.n {
		b := New(a.cap + 1)
		if a.n == a.cap && a.cap != 0 {
			b = New(2 * a.cap)
		}
		for e := 0; e < i; e++ {
			b.elems[e] = a.elems[e]
		}
		b.elems[i] = x
		for e := i; e < a.n; e++ {
			b.elems[e+1] = a.elems[e]
		}
		a.elems, a.cap, a.n = b.elems, b.cap, a.n+1
		return nil
	} else {
		return errors.New("Index out of range")
	}
}

// Push inserts an element to the right end of the array
func (a *Array) Push(x Element) error {
	if a.n < a.cap && a.cap != 0 {
		a.elems[a.n], a.n = x, a.n+1
		return nil
	}
	b := New(a.cap + 1)
	if a.n == a.cap && a.cap != 0 {
		b = New(2 * a.cap)
	}
	for e := 0; e < a.n; e++ {
		b.elems[e] = a.elems[e]
	}
	b.elems[a.n] = x
	a.elems, a.cap, a.n = b.elems, b.cap, a.n+1
	return nil
}

// Delete removes an element from the array by index
func (a *Array) Delete(i int) error {
	if a.n == 0 || a.cap == 0 || i >= a.n || i >= a.cap {
		return errors.New("Index out of range")
	}
	if a.n == 1 {
		a.elems, a.n = make([]Element, 0), 0
	}
	if a.n > 1 && a.n != a.cap/2 {
		for e := i; e < a.cap-1; e++ {
			a.elems[e] = a.elems[e+1]
		}
		a.n -= 1
		return nil
	}
	if a.n > 1 && a.n == a.cap/2 {
		b := New(a.cap / 2)
		for e := 0; e < i; e++ {
			b.elems[e] = a.elems[e]
		}
		for e := i + 1; e < a.n; e++ {
			b.elems[e-1] = a.elems[e]
		}
		a.elems, a.cap, a.n = b.elems, b.cap, a.n-1
		return nil
	}
	return errors.New("Index out of range")
}

// Pop deletes the last element of the array
func (a *Array) Pop() error {
	if a.n == 0 || a.cap == 0 {
		return errors.New("Index out of range")
	}
	var c int
	if a.n-1 == a.cap/2 {
		c = a.cap / 2
	} else {
		a.elems[a.n-1], a.n = 0, a.n-1
		return nil
	}
	b := New(c)
	for e := 0; e < a.n-1; e++ {
		b.elems[e] = a.elems[e]
	}
	a.elems, a.cap, a.n = b.elems, b.cap, a.n-1
	return nil
}

// String returns a textual representation of the array
func (a *Array) String() string {
	if a.Len() == 0 {
		return "[]"
	}
	s := "["
	for i := 0; i < a.n-1; i++ {
		s = s + strconv.FormatUint(uint64(a.elems[i]), 10) + ", "
	}
	s += strconv.FormatUint(uint64(a.elems[a.n-1]), 10) + "]"
	return s
}
