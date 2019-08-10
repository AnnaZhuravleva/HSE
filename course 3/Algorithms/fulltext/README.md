# Simple Full Text Search

Given an array of "documents", build a data structure that implements a simple full text search.

* Documents are non-empty strings of lowercase words divided by spaces.
* Each document has an implicit *identifier* equal to its index in the input array.
* `New()` constructs the index.
* `Search()`:
    * accepts a query, which is also a string of lowercase words divided by spaces;
    * returns a sorted array of unique *identifiers* of documents that contains *all* words from the query regardless of their order.

```golang
index := New([]string{
    "this is the house that jack built",  //: 0
    "this is the rat that ate the malt",  //: 1
)

index.Search("")  // -> []
index.Search("in the house that jack built")  // -> []
index.Search("malt rat")  // -> [1]
index.Search("is this the")  // -> [0, 1]
```
