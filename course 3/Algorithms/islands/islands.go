package islands

func tmp(grid [][]uint8, r int, c int) {
	grid[r][c] = 0
	if r < len(grid)-1 && grid[r+1][c] == 1 {
		tmp(grid, r+1, c)
	}
	if c < len(grid[0])-1 && grid[r][c+1] == 1 {
		tmp(grid, r, c+1)
	}
	if c >= 1 && grid[r][c-1] == 1 {
		tmp(grid, r, c-1)
	}
	if r >= 1 && grid[r-1][c] == 1 {
		tmp(grid, r-1, c)
	}
}

// CountIslands returns the number of islands on a 2D grid maps
func CountIslands(grid [][]uint8) int {
	c := 0
	if len(grid) != 0 {
		for i := 0; i < len(grid); i++ {
			for j := 0; j < len(grid[0]); j++ {
				if grid[i][j] == 1 {
					tmp(grid, i, j)
					c++
				}
			}
		}
	}
	return c
}
