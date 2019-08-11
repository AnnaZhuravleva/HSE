package streamlatest

// Stream accepts integers and allows to get any of `k` latest of them in O(1)
type Stream struct {
	k   int
	pos int
	arr []int
}

// New creates a Stream instance
func New(k int) *Stream {
	if k < 1 {
		panic("invalid argument, expected to save at least one latest element")
	}
	return &Stream{k, 0, make([]int, k)}
}

// Push adds an integer to the stream
func (s *Stream) Push(value int) {
	s.arr[s.pos%s.k] = value
	s.pos += 1
}

// Latest returns the `i`th latest element (zero-based) and a boolean that indicates success
func (s *Stream) Latest(i int) (int, bool) {
	if s.pos == 0 || i >= s.k || i < 0 || i >= s.pos {
		return -1, false
	}
	idx := (s.pos-1)%s.k - i
	if idx < 0 {
		idx += s.k
	}
	return s.arr[idx], true
}
