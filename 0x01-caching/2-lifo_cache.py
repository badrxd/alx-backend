#!/usr/bin/env python3
'''LIFO Caching system'''
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    '''class of LIFO caching system'''
    items = {}

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key
        '''
        if key is None or item is None:
            return
        ln = len(self.cache_data)
        keys = list(self.cache_data.keys())

        if ln >= self.MAX_ITEMS:
            if key in keys:
                self.cache_data.pop(key)
            else:
                self.cache_data.pop(keys[-1])
                print("DISCARD: {}".format(keys[-1]))

        self.cache_data[key] = item

    def get(self, key):
        '''return the value in self.cache_data linked to key'''
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data[key]
