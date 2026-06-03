package main

import (
	"fmt"
	"sort"
)

type Ride struct {
	Start    int
	Duration int
	End      int
}

func solve(landStartTime, landDuration []int, waterStartTime, waterDuration []int) int {
	n, m := len(landStartTime), len(waterStartTime)
	land := make([]Ride, n)
	for i := 0; i < n; i++ {
		land[i] = Ride{landStartTime[i], landDuration[i], landStartTime[i] + landDuration[i]}
	}
	water := make([]Ride, m)
	for j := 0; j < m; j++ {
		water[j] = Ride{waterStartTime[j], waterDuration[j], waterStartTime[j] + waterDuration[j]}
	}

	ans := int(^uint(0) >> 1)

	// Order A: Land -> Water
	sort.Slice(land, func(i, j int) bool { return land[i].End < land[j].End })
	for _, w := range water {
		idx := sort.Search(len(land), func(i int) bool { return land[i].End > w.Start })
		if idx > 0 {
			if c := w.Start + w.Duration; c < ans { ans = c }
		}
		if idx < len(land) {
			if c := land[idx].End + w.Duration; c < ans { ans = c }
		}
	}

	// Order B: Water -> Land
	sort.Slice(water, func(i, j int) bool { return water[i].End < water[j].End })
	for _, l := range land {
		idx := sort.Search(len(water), func(i int) bool { return water[i].End > l.Start })
		if idx > 0 {
			if c := l.Start + l.Duration; c < ans { ans = c }
		}
		if idx < len(water) {
			if c := water[idx].End + l.Duration; c < ans { ans = c }
		}
	}
	return ans
}

func main() {
	fmt.Printf("Ex1: %d (expected 9)\n", solve([]int{2,8}, []int{4,1}, []int{6}, []int{3}))
	fmt.Printf("Ex2: %d (expected 14)\n", solve([]int{5}, []int{3}, []int{1}, []int{10}))
}
