package main

import "testing"

func TestSolve(t *testing.T) {
	cases := []struct {
		n string; ls, ld, ws, wd []int; e int
	}{
		{"Ex1", []int{2,8}, []int{4,1}, []int{6}, []int{3}, 9},
		{"Ex2", []int{5}, []int{3}, []int{1}, []int{10}, 14},
		{"Land first", []int{0}, []int{2}, []int{10}, []int{5}, 15},
		{"Water first", []int{10}, []int{5}, []int{0}, []int{2}, 15},
		{"Overlap", []int{0}, []int{5}, []int{2}, []int{4}, 9},
		{"Multi", []int{1,10}, []int{3,2}, []int{5,15}, []int{2,1}, 7},
		{"Fallback", []int{0,100}, []int{1,1}, []int{50}, []int{5}, 55},
		{"Same", []int{0}, []int{5}, []int{0}, []int{5}, 10},
	}
	for _, c := range cases {
		t.Run(c.n, func(t *testing.T) {
			if g := solve(c.ls, c.ld, c.ws, c.wd); g != c.e {
				t.Errorf("got %d, want %d", g, c.e)
			}
		})
	}
}
