# Islands

Count the number of islands on a grid map represented by 2D array (in our case, array of arrays). The array contains 1s (land) and 0s (water). An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

The function can (and probably should) mutate the original array. Reference solution uses depth-first search.

```golang
CountIslands(
    [][]uint8{
        []uint8{0, 0, 1},
        []uint8{0, 0, 1},
        []uint8{0, 1, 0},
    },
)  # -> 2

CountIslands(
    [][]uint8{
        []uint8{1, 1, 1},
        []uint8{0, 0, 1},
        []uint8{0, 1, 1},
    },
)  # -> 1
```