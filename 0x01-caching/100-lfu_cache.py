#!/usr/bin/env python3
'''MRU Caching system'''
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    '''class of MRU caching system'''

    frequency = {}

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key
        '''
        if key is None or item is None:
            return

        if self.get(key) != item:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                k = min(self.frequency, key=self.frequency.get)
                self.cache_data.pop(k)
                print('DISCARD:', k)
                self.frequency.pop(k)
            if key not in self.frequency:
                self.frequency[key] = 0

    def get(self, key):
        '''return the value in self.cache_data linked to key'''
        if key is None or key not in self.cache_data.keys():
            return None
        self.frequency[key] += 1
        return self.cache_data[key]
