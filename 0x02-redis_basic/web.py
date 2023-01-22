#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

redis = redis.Redis()


def outter(fn):
    @wraps(fn)
    def inner(url):

        cached = redis.get(f"cache:{url}")
        if cached:
            return cached.decode("utf-8")
        redis.incr(f"count:{url}")
        result = fn(url)
        redis.setex(f"cached{url}", 10, result)
        return result
    return inner


@outter
def get_page(url: str) -> str:
    """get page self descriptive
    """
    response = requests.get(url)
    return response.text
