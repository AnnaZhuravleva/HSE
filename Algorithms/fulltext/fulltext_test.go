package fulltext

import (
	"reflect"
	"testing"
)

func TestUnit__Basic(t *testing.T) {

	idx := New([]string{
		"this is the house that jack built",
		"this is the malt that lay in the house that jack built",
		"this is the rat that ate the malt",
		"that lay in the house that jack built",
		"this is the cat",
		"that killed the rat that ate the malt",
		"that lay in the house that jack built",
	})

	if !reflect.DeepEqual(idx.Search("this"), []int{0, 1, 2, 4}) {
		t.Fatal()
	}

	if !reflect.DeepEqual(idx.Search("this is the cat"), []int{4}) {
		t.Fatal()
	}

	if !reflect.DeepEqual(idx.Search("jack that lay"), []int{1, 3, 6}) {
		t.Fatal()
	}

	if !reflect.DeepEqual(idx.Search(""), []int{}) {
		t.Fatal()
	}

	if !reflect.DeepEqual(idx.Search("farmer sowing his corn"), []int{}) {
		t.Fatal()
	}
}
