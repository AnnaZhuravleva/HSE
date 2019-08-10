package streamlargest

import "errors"

// Stream accepts integers and allows to get `k` largest of them in O(1)
type Stream struct {
	k   int
	pos int
	arr []int
}

// New creates a Stream instance
func New(k int) (*Stream, error) {
	if k < 1 {
		return nil, errors.New("invalid argument, expected to save at least one latest element")
	}
	return &Stream{k, 0, make([]int, k)}, nil
}

// Push adds an integer to the stream
func (s *Stream) Push(value int) {
	s.pos++
	if value < s.arr[0] {
		return
	}
	if s.arr[s.k-1] <= value {
		copy(s.arr[:s.k-1], s.arr[1:s.k])
		s.arr[s.k-1] = value
		return
	} else {
		for i := 0; i < s.k; i++ {
			if value >= s.arr[i] && value < s.arr[i+1] {
				copy(s.arr[:i], s.arr[1:i+1])
				s.arr[i] = value
				return
			}
		}
	}

}

// Largest get at most `k` largest elements from the stream in arbitraty order
func (s *Stream) Largest() []int {
	if s.pos < s.k {
		new := make([]int, s.pos)
		copy(new, s.arr[s.k-s.pos:])
		return new
	}
	new := make([]int, s.k)
	copy(new, s.arr)
	return new
}
