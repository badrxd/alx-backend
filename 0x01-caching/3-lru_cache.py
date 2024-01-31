#!/usr/bin/env python3
'''LRU Caching system'''
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    '''class of LRU caching system'''

    def __init__(self):
        super().__init__()
        self.items = {}
        self.counter = 0

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key
        '''
        if key is None or item is None:
            return
        ln = len(self.cache_data)

        if ln >= self.MAX_ITEMS:
            keys = list(self.cache_data.keys())
            min_count = min(self.items, key=self.items.get)
            if key in keys:
                self.cache_data.pop(key)
                self.items.pop(key)
            else:
                self.cache_data.pop(min_count)
                self.items.pop(min_count)
                print("DISCARD: {}".format(min_count))

        self.cache_data[key] = item
        self.items[key] = self.counter
        self.counter += 1

    def get(self, key):
        '''return the value in self.cache_data linked to key'''
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
