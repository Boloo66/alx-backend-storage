#!/usr/bin/env python3
"""Redis module task 0
"""
import redis
from typing import Union, Callable, Optional, Any
from uuid import uuid4
import functools


def call_history(method: Callable) -> Callable:
    """ creates a list of parameters and return values """
    @functools.wraps(method)
    def inner(self, *args, **kwargs):
        """my inner func """
        for _ in args:
            self._redis.rpush(method.__qualname__+":inputs", _)

        r_val = str(method(self, *args, **kwargs))

        self._redis.rpush(method.__qualname__+":outputs", r_val)
        return r_val
    return inner


def count_calls(method: Callable) -> Callable:
    """ Counts the number of times a function is called """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ my inner func """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


'''
def replay(fn: Any):
    """ Shows the number of calls, parameter and values """
    self_ = fn.__self__
    func_name = fn.__qualname__
    n_times = self_.get_str(func_name)
    print("{} was called {} times".format(func_name, n_times))
    """ TODO: print input and output from call history decorator function """
    inputs = self_._redis.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = self_._redis.lrange("{}:outputs".format(func_name), 0, -1)

    for i, o in zip(inputs, outputs):
        try:
            para = i.decode("utf-8")
        except Exception:
            para = ""
        try:
            value = o.decode("utf-8")
        except Exception:
            value = ""

        print("{}(*({})) -> {}".format(func_name, para, value))
'''


def call_history(method: Callable) -> Callable:
    """ number of history inputs"""
    inputs = method.__qualname__ + ":inputs"
    outputs = method.__qualname__ + ":outputs"

    @functools.wraps(method)
    def wrapper(self, *args, **kwds):
        """wrapper of decorator"""
        self._redis.rpush(inputs, str(args))
        returned_method = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(returned_method))
        return returned_method
    return wrapper


class Cache:
    """ This class creates a cache file """

    def __init__(self) -> None:
        """ Instance of an obj """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ creates and store a key and maps it to a data para"""
        mkey = str(uuid4())
        self._redis.set(mkey, data)
        return mkey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ returns a value of key """
        val = self._redis.get(key)
        if fn:
            val = fn(val)
        return val

    def get_str(self, key: str) -> str:
        """ gets decoded str instead of bytes from rdb"""
        val = self._redis.get(key)
        return val.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ gets an int from a rdb """
        val = self._redis.get(key)
        try:
            val = val.decode("utf-8")
        except Exception:
            val = 0
        return int(val)
