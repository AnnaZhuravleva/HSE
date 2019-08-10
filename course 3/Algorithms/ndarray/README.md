# N-Dimensional Array

`NDArray` represents a prototype of static n-dimensional array/matrix defined with a list of its axes:

```golang
New(10)  // 1D array of length 10
New(10, 10)  // 2D matrix 10x10
New(3, 3, 3, 3)  // 4-dimensional cube with edges of size 3
```

It is assumed that the array elements are stored linearly using [row-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order).

Implement the method `.Idx()` so that it returns an index in the linearised array for a given n-dimensional index. For example:

```golang
matrix := New(3, 3)  // 2D matrix 3x3

// The matrix would look like this:
// | 2, 1, 2 |
// | 8, 5, 0 |
// | 6, 0, 0 |

// Same thing stored in row-major manner:
// [2, 1, 2, 8, 5, 0, 6, 0, 0]

// 2D index (1, 1) gives the central element, which is 5.
// Its index in the linearised array is 4. So is returned by Idx: 

matrix.Idx(1, 1)  // -> 4
```
