# coding: utf-8
# @Time : 12/22/21 1:57 PM

import time
from functools import lru_cache


class LruCache:

    def __init__(self, maxsize=3, timeout=2):
        self.maxsize = maxsize
        self.timeout = timeout
        self.last_time = int(time.time())

    def __call__(self, func):

        func = lru_cache(maxsize=self.maxsize)(func)

        def wrapper(*args, **kwargs):
            if int(time.time()) - self.last_time > self.timeout:
                func.cache_clear()
                self.last_time = int(time.time())
            return func(*args, **kwargs)
        return wrapper
