package distance

// EditDistance computes the minimal number of operations "add", "delete", and "replace" to transform `s1` into `s2`
func EditDistance(s1, s2 string) int {
	if len(s1) == 0 {
		return len(s2)
	}
	if len(s2) == 0 {
		return len(s1)
	}
	var table [1000][1000]int
	var cost int
	minValue := func(x, y, z int) int {
		c := x
		if y < c {
			c = y
		}
		if z < c {
			c = z
		}
		return c
	}
	for i := 1; i < len(s1); i++ {
		table[i][0] = i
	}
	for j := 1; j < len(s2); j++ {
		table[0][j] = j
	}
	for j := 1; j <= len(s2); j++ {
		for i := 1; i <= len(s1); i++ {
			if s1[i-1] == s2[j-1] {
				cost = 0
			} else {
				cost = 1
			}
			table[i][j] = minValue((table[i-1][j] + 1), (table[i][j-1] + 1), (table[i-1][j-1] + cost))
		}
	}
	return table[len(s1)][len(s2)]
}
