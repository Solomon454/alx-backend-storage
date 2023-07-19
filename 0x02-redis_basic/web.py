#!/usr/bin/env python3
"""A module with tools for request caching and tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable


import requests
import functools
import time

# Decorator for caching with a time-to-live (TTL)
def expiring_cache(ttl):
    def decorator(func):
        cache = functools.lru_cache(maxsize=None, typed=False)

        @functools.wraps(func)
        def wrapper(url):
            result = cache.get(url)
            if result is None:
                result = func(url)
                cache[url] = result
                time.sleep(ttl)  # Simulate a slow response time for the slowwly API
            return result

        return wrapper

    return decorator

# Decorator with a default TTL of 10 seconds
def cache_with_default_ttl(func):
    return expiring_cache(10)(func)

# Get the HTML content of a URL and track the number of accesses
@cache_with_default_ttl
def get_page(url):
    # Simulate a slow response using slowwly API
    slowwly_url = f"http://slowwly.robertomurray.co.uk/delay/1000/url/{url}"
    response = requests.get(slowwly_url)

    # Increment the access count for this URL
    access_count_key = f"count:{url}"
    access_count = int(redis_client.get(access_count_key) or 0)
    redis_client.set(access_count_key, access_count + 1)

    return response.text

if __name__ == "__main__":
    # Test the get_page function
    print(get_page("https://www.mysolomon.com"))
    print(get_page("https://www.google.com"))
    print(get_page("https://www.redmart.com"))
