# Any of k Latest Elements in a Stream

Implement a `Stream(k)` data structure that supports two operations:

* `Push(x)` — adds an integer into the stream in `O(1)` time.
* `Latest(i)` for `i < k` returns the i'th (zero-based) latest elements from the stream in `O(1)` time.

After any number of pushes the stream is expected to take `O(k)` space.

```go
stream, err := New(3)

stream.Push(1)
stream.Push(2)
v, ok := stream.Latest(0) // -> 2, true
v, ok = stream.Latest(1) // -> 1, true
v, ok = stream.Latest(2) // -> -1, false (not enough elements)
v, ok = stream.Latest(3) // -> -1, false (out of range)
```
