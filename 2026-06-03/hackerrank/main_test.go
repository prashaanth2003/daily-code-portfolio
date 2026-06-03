package main

import "testing"

func TestDD(t *testing.T) {
	cases := []struct {
		n string; m [][]int32; e int32
	}{
		{"Ex", [][]int32{{1,2,3},{4,5,6},{9,8,9}}, 2},
		{"1x1", [][]int32{{5}}, 0},
		{"2x2", [][]int32{{1,2},{3,4}}, 0},
		{"Zero", [][]int32{{0,0,0},{0,0,0},{0,0,0}}, 0},
		{"Neg", [][]int32{{-1,1,-7},{-8,10,8},{-3,4,5}}, 14},
		{"4x4", [][]int32{{11,2,4,2},{4,5,6,8},{10,8,-12,1},{1,2,3,4}}, 3},
		{"Alt", [][]int32{{1,2},{4,1}}, 4},
		{"Large", [][]int32{{1000000,0},{0,1000000}}, 2000000},
	}
	for _, c := range cases {
		t.Run(c.n, func(t *testing.T) {
			if g := diagonalDifference(c.m); g != c.e {
				t.Errorf("got %d, want %d", g, c.e)
			}
		})
	}
}
