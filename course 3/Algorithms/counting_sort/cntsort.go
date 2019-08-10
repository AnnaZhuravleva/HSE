package cntsort

func CountingSort(values []int) {
	if len(values) == 0 {
		return
	}
	max, min := values[0], values[0]
	for i, v := range values {
		if values[i] > max {
			max = v
		}
		if min > values[i] {
			min = v
		}
	}
	k := max - min
	key := func(v int) int { return v - min }
	output, count := make([]int, len(values)), make([]int, k+1)
	for _, i := range values {
		count[key(i)] += 1
	}
	for i := 1; i < k+1; i++ {
		count[i] = count[i-1] + count[i]
	}
	for i := len(values); i > 0; i-- {
		output[count[key(values[i-1])]-1] = values[i-1]
		count[key(values[i-1])]--
	}
	copy(values, output)
}
