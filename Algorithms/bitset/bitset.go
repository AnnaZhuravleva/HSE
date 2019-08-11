package bitset

import "errors"

// Bitset is fixed-size sequence of `size` bits
type Bitset struct {
	size int
	set  []uint64
}

const f = uint(64) - 1
const s = uint(6)
const maxw = 1<<64 - 1
const mm1 = (maxw / 15 * 3)
const mm2 = maxw / 255 * 15
const mm3 = maxw / 255
const mm4 = 56
const m5 = maxw / 3

// New creates a new Bitset of a given size
func New(size int) *Bitset {
	Size := func(i int) int {
		if uint(i) > (^uint(0) - f + 2) {
			return int(^uint(0) >> s)
		}
		return int((uint(i) + (f)) >> s)
	}
	return &Bitset{size, make([]uint64, Size(size))}
}

// Set sets a specific bit
func (b *Bitset) Set(pos int, value bool) error {
	if (pos < 0) || (pos >= b.size) {
		return errors.New("error")
	}
	if value == true {
		b.set[uint(pos)>>s] |= 1 << uint(pos%64)
	} else {
		b.set[uint(pos)>>s] &^= 1 << (uint(pos%64) & (f))
	}
	return nil
}

// Test returns a value of specific bit
func (b *Bitset) Test(pos int) (bool, error) {
	if (pos < 0) || (pos >= b.size) {
		return false, errors.New("Index out of range")
	}
	return b.set[uint(pos)>>s]&(1<<(uint(pos%64)&(f))) != 0, nil
}

// Count is returns the number of bits set to `true`
func (b *Bitset) Count() int {
	var nb int
	oc2 := func(w uint64) int {
		w -= (w >> 1) & m5
		w = w&mm1 + (w>>2)&mm1
		w += w >> 4
		w &= mm2
		w *= mm3
		w >>= mm4
		return int(w)
	}
	for _, i := range b.set {
		if i != 0 {
			nb += oc2(i)
		}
	}
	return int(nb)
}

// All checks if all bits are set to `true`
func (b *Bitset) All() bool {
	return b.Count() == b.size
}

// Any checks if there is at least one bit set to `true`
func (b *Bitset) Any() bool {
	if b != nil && b.set != nil {
		for _, w := range b.set {
			if w > 0 {
				return true
			}
		}
		return false
	}
	return false
}

// Flip toggles the values of bits
func (b *Bitset) Flip() {
	for i := range b.set {
		b.set[i] = ^b.set[i]
	}
	return
}

// Reset sets all bits to `false`
func (b *Bitset) Reset() {
	for i, _ := range b.set {
		b.set[i] = 0
	}
	return
}
