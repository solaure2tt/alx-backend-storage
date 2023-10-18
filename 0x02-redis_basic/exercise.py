#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from typing import Union, Callable, Any, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


class Cache:
    """ initialisation of redis and storage of a data"""
    def __init__(self):
        """ Instancaition of redis client as private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """generate a random key (e.g. using uuid),
            store the input data in Redis
            args:
              data: parameter to stor in redis
            return:
              a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, int, float, bytes]:
        """convert the data back to the desired format
           args:
             key: sstring argument
             fn: callable used to convert the data back to the desired format
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get with
           the correct conversion function
           args:
             key: string argument
            return:
               a string
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get with
           the correct conversion function
           args:
             key: string argument
            return:
               a string
        """
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data


def replay(method: Callable):
    """function to display the history of calls
       of a particular function
    """
    key = method.__qualname__
    inps = key + ":inputs"
    outs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inpsList = redis.lrange(inps, 0, -1)
    outsList = redis.lrange(outs, 0, -1)
    zipped = list(zip(inpsList, outsList))
    for a, b in zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
