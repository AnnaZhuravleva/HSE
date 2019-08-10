package queue

import "errors"

// MaxQueue is a FIFO queue that allows fast queries for the maximum among currently enqueued elements.
type MaxQueue struct {
	nodes     []uint32
	maxvalues []uint32
	cap       int
	head      int
	tail      int
}

// New creates an instance of MaxQueue
func New() *MaxQueue { return new(MaxQueue) }

// Push inserts and element to the tail
func (q *MaxQueue) Push(value uint32) {
	q.nodes, q.cap = append(q.nodes, value), q.cap+1
	if q.tail == 0 {
		q.maxvalues = append(q.maxvalues, value)
	} else {
		m := q.maxvalues[q.tail-1]
		if value > m {
			m = value
		}
		q.maxvalues = append(q.maxvalues, m)
	}
	q.tail++
	return
}

// Pop removes an element from the head
func (q *MaxQueue) Pop() (uint32, error) {
	if q.tail == 0 || q.cap == 0 || q.head >= q.tail || q.head == q.cap {
		return 0, errors.New("error")
	}
	r := q.nodes[q.head]
	q.head++
	if r == q.maxvalues[q.tail-1] && q.tail >= 2 {
		q.maxvalues[q.tail-1] = q.maxvalues[q.tail-2]
	}
	if q.tail-1 == q.head {
		q.maxvalues[q.tail-1] = q.nodes[q.tail-1]
	}
	return r, nil
}

// Max returns maximum among currently enqueued elements
func (q *MaxQueue) Max() (uint32, error) {
	if q.tail == 0 || q.head >= q.tail {
		return 0, errors.New("empty queue!")
	}
	return q.maxvalues[q.tail-1], nil
}
