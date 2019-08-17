# k Largest Elements in a Stream

Implement a `Stream(k)` data structure that supports two operations:

* `Push(x)` — adds an integer into the stream in `O(log k)` time.
* `Largest()` — returns an array of at most `k` largest elements from the stream in *arbitraty* order in `O(1)` time.

After any number of pushes the stream is expected to take `O(k)` space.

```golang
stream, err := New(2)

stream.Push(4)
stream.Largest() // -> [4]

stream.Push(1)
stream.Push(10)
stream.Largest() // -> [4, 10]

stream.Push(5)
stream.Push(11)
stream.Largest() // -> [5, 11]
```

* `Largest()` is expected to return a newly allocated array holding the result.
* You can use `container/heap` package from go's stardard library.
