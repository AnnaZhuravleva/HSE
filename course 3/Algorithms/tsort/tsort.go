package tsort

import (
	"errors"
	"sort"
	"strconv"
)

// THE FILE MUST CONTAIN A SINGLE FUNCTION DEFINITION
// TSort performs a topological sort on the given graph represented as a list of edges
func TSort(edges []string) ([]string, error) {
	if len(edges) == 0 {
		return edges, nil
	}
	if len(edges)%2 != 0 {
		return nil, errors.New("Odd number of elements")
	}
	inEdges := make(map[int]map[int]struct{})
	outEdges := make(map[int]map[int]struct{})
	for i, _ := range edges {
		if i%2 == 0 {
			a, _ := strconv.Atoi(edges[i])
			b, _ := strconv.Atoi(edges[i+1])
			if _, ok := inEdges[a]; !ok {
				inEdges[a] = make(map[int]struct{})
			}
			inEdges[a][b] = struct{}{}
			if _, ok := outEdges[b]; !ok {
				outEdges[b] = make(map[int]struct{})
			}
			outEdges[b][a] = struct{}{}
		}
	}
	s := make(map[int]struct{})
	for m := range outEdges {
		if len(inEdges[m]) == 0 {
			s[m] = struct{}{}
		}
	}
	var l []int
	for len(s) > 0 {
		var n int
		for n = range s {
			break
		}
		delete(s, n)
		l = append(l, n)
		for m := range outEdges[n] {
			delete(outEdges[n], m)
			delete(inEdges[m], n)
			if len(inEdges[m]) == 0 {
				s[m] = struct{}{}
			}
		}
	}
	for _, es := range inEdges {
		if len(es) > 0 {
			return nil, errors.New("has cycle")
		}
	}
	var res []string
	sort.Ints(l)
	for _, v := range l {
		res = append(res, strconv.Itoa(v))
	}
	return res, nil
}
