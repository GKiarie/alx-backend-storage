#!/usr/bin/env python3
"""Cacha class"""
import redis
import uuid
from typing import Union


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
