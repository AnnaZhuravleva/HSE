package lru

import (
	"container/list"
)

type Item struct {
	Key   int
	Value int
}

// Cache represents an fixed-size LRU cache for integer keys and values
type Cache struct {
	capacity int
	items    map[int]*list.Element
	queue    *list.List
}

// New returns an initialised LRU cache for the given capacity
func New(capacity int) *Cache {
	return &Cache{
		capacity: capacity,
		items:    make(map[int]*list.Element),
		queue:    list.New(),
	}
}

// Get returns a cached value for the given key, or -1 if the key does not exist
func (cache *Cache) Get(key int) int {
	element, exists := cache.items[key]
	if exists == false {
		return -1
	}
	cache.queue.MoveToFront(element)
	return element.Value.(*Item).Value
}

// Put inserts or updates the value for the given key.
// When the cache capacity is reached, it removes the least recently used item before inserting a new one.
func (cache *Cache) Put(key int, value int) {
	purge := func(c *Cache) {
		if element := cache.queue.Back(); element != nil {
			item := cache.queue.Remove(element).(*Item)
			delete(cache.items, item.Key)
		}
	}
	if element, exists := cache.items[key]; exists == true {
		cache.queue.MoveToFront(element)
		element.Value.(*Item).Value = value
		return
	}
	if cache.queue.Len() == cache.capacity {
		purge(cache)
	}
	item := &Item{
		Key:   key,
		Value: value,
	}
	element := cache.queue.PushFront(item)
	cache.items[item.Key] = element
	return
}
