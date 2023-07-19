#!/usr/bin/env python3
"""Cacha class"""
import redis
import uuid
from typing import Union, Callable
import functools
import ast


def count_calls(method: Callable) -> Callable:
    """Ftn that returns a callable"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store history of inputs & outputs"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Append the input arguments to the input list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in the output list
        self._redis.rpush(output_key, output)

        return output

    return wrapper


def replay(method: Callable):
    """ftn to display history of calls"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    inputs = [ast.literal_eval(args_str.decode())
              for args_str in cache._redis.lrange(input_key, 0, -1)]
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{args}) -> {output.decode()}")


class Cache:
    def __init__(self):
        """Initialize a Redis client
        and flush the instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate a random key using uuid"""
        key = str(uuid.uuid4())

        # Store the data in Redis using the generated key
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int]:
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)
