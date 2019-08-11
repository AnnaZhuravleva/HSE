# LRU Cache

Implement and design a data structure for [Least Recently Used (LRU) cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU).

Out version of the cache represents a key-value storage holding a fixed number of items (capacity). Both key and value are integers. Two operations are supported:

* `Get(key)`: fetch the value of the key if the key exists in the cache, otherwise return `-1`.
* `Put(key, value)`: insert or update the key with the given value.

```golang
c := New(3)  // LRU cache of size 3
c.Put(1, 100)
c.Put(2, 200)
c.Put(3, 300)
c.Get(1)  // -> 100
```

If the number of items in the cache exceed its capacity, **`Put` removes the least recently used key before inserting a new one**. The key is "used" every time it is fetched with `Get` or its value is updated with `Put`.

```golang
c := New(2)

c.Put(1, 100)
c.Put(2, 200)
c.Put(3, 300)

c.Get(1)  // -> -1, the key was removed

c.Get(2)  // "use" the key
c.Put(4, 400)  // removes `3` because `2` was used recently.

c.Put(2, 200)  // "use" the key
c.Put(5, 500)  // removes `4`, `2` is still there
```

You will probably need [container/list](https://golang.org/pkg/container/list/) package.