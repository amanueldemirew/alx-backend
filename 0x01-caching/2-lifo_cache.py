#!/usr/bin/env python3
"""
LIFOCache module
"""
from collections import deque
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFO based caching system
    """
    def __init__(self):
        """
        Initialize
        """
        super().__init__()
        self.lifo = deque()

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(self.lifo[-1]))
            del self.cache_data[self.lifo[-1]]
            self.lifo.pop()

        try:
            self.lifo.remove(key)

        except ValueError:
            pass

        self.lifo.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key)
