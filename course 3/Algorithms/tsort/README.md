# Topological Sort

Implement a [topological sorting](https://en.wikipedia.org/wiki/Topological_sorting) algorithm.

* **The solution must contain a single function (`TSort`).** This implies that recursive implementations are not allowed.
* The input graph is represented as an array of vertices in which each consecutive pair makes an edge in the graph.
    * For example, the input `["a", "b", "c", "d", "e", "f", "b", "c", "d", "e"]` represents a graph with the following edges: `<a,b>`, `<c,d>`, `<e,f>`, `<b,c>`, `<d,e>`.
    * An odd number of elements in the array results in an error.
* An error must be returned for cyclic graphs.
* A graph can have more than one topological sorting. Your algorithm can pick any of them as long as it is valid.
* `tsort` command line utility ([see docs](https://www.gnu.org/software/coreutils/manual/html_node/tsort-invocation.html)) works the same way; you may find it useful for a reference.

```golang
TSort([]string{"a", "b", "c", "d", "e", "f", "b", "c", "d", "e"}) 
// -> ["a", "b", "c", "d", "e", "f"]
```
