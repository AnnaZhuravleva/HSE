package fulltext

import "strings"

// Index implements fulltext  search
type Index struct {
	Documents map[string][]int
}

func unique(values []int) []int {
	var count int
	for i := 1; i < len(values); i++ {
		if values[count] == values[i] {
			continue
		}
		count++
		values[count] = values[i]
	}
	return values[:count+1]
}

// New creates a fulltext search index for the given documents
func New(docs []string) *Index {
	dict := new(Index)
	dict.Documents = make(map[string][]int)
	for i := range docs {
		for _, word := range strings.Fields(docs[i]) {
			dict.Documents[word] = append(dict.Documents[word], i)
		}
	}
	for w := range dict.Documents {
		dict.Documents[w] = unique(dict.Documents[w])
	}
	return dict
}

func intersect(a []int, b []int) []int {
	res := []int{}
	var i, k int
	for i < len(a) && k < len(b) {
		if a[i] < b[k] {
			i++
		} else if a[i] > b[k] {
			k++
		} else {
			res = append(res, a[i])
			i++
			k++
		}
	}
	return res
}

// Search returns a slice of unique ids of documents that contains all words from the query.
func (idx *Index) Search(query string) []int {
	if query == "" {
		return []int{}
	}
	words := strings.Fields(query)
	res, ok := idx.Documents[words[0]]
	if ok == false {
		return []int{}
	}
	for _, v := range words[1:] {
		_, ok := idx.Documents[v]
		if ok {
			res = intersect(res, idx.Documents[v])
		} else {
			return []int{}
		}
	}
	return res
}
