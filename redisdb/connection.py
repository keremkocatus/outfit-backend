import os
import redis.asyncio as redis
from core.config import REDIS_URL

class RedisConnection:
    _client: redis.Redis | None = None

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            redis_url = REDIS_URL
            if not redis_url:
                raise ValueError("REDIS_URL environment variable is missing.")

            cls._client = redis.from_url(
                redis_url,
                decode_responses=True,   
                max_connections=20,      # Connection pool
            )
        return cls._client

redis_client: redis.Redis = RedisConnection.get_client()
