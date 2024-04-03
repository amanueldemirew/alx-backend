#!/usr/bin/env python3
"""
BasicCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    Dictionary based caching system
    """
    def put(self, key, item):
        """
        Add the item in the cache
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key)
