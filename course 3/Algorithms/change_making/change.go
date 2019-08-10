package tree

func findmin(coins []int) int {
	c := coins[0]
	for _, v := range coins {
		if v < c {
			c = v
		}
	}
	return c
}

// Change computes an optimal number of coins from a given set that cover a given amount.
func Change(coins []int, amount int) int {
	if len(coins) == 0 && amount != 0 {
		return -1
	}
	if amount > 0 && amount <= findmin(coins) && len(coins) != 0 {
		return 1
	}
	array := make([]int, amount+1)
	for i := 0; i <= amount; i++ {
		count := i
		for _, v := range coins {
			if v <= i {
				if array[i-v]+1 < count {
					count = array[i-v] + 1
				}
			}
		}
		array[i] = count
	}
	return array[amount]
}
