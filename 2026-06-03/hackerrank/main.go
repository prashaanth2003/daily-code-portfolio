package main

import (
	"fmt"
	"math"
)

func diagonalDifference(arr [][]int32) int32 {
	var l, r int32
	for i := 0; i < len(arr); i++ {
		l += arr[i][i]
		r += arr[i][len(arr)-1-i]
	}
	return int32(math.Abs(float64(l - r)))
}

func main() {
	m := [][]int32{{1,2,3},{4,5,6},{9,8,9}}
	fmt.Printf("Diff: %d (expected 2)\n", diagonalDifference(m))
}
