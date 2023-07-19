#!/usr/bin/env python3
"""Cacha class"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    def __init__(self):
        """Initialize a Redis client
        and flush the instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
