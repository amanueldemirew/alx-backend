#!/usr/bin/env python3
"""
FIFOCache Module
"""
from collections import deque
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFO Based caching system
    """
    def __init__(self):
        """
        Initialize
        """
        super().__init__()
        self.fifo = deque()

    def put(self, key, item):
        """
        Add the item in the cache
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if key not in self.cache_data:
            self.fifo.append(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(self.fifo[0]))
            del self.cache_data[self.fifo[0]]
            self.fifo.popleft()

        try:
            self.fifo.remove(key)

        except ValueError:
            pass

        self.fifo.append(key)

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key)
