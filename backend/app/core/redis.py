"""Redis client configuration with in-memory fallback."""
from __future__ import annotations

import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Try to import redis, fallback to None if not installed
try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("redis not installed, using in-memory fallback")


class RedisClient:
    """Redis client with in-memory fallback for development."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0", prefix: str = "mangatarem:"):
        self.redis_url = redis_url
        self.prefix = prefix
        self._redis = None
        self._memory_store: dict[str, str] = {}  # In-memory fallback
    
    async def connect(self):
        """Connect to Redis."""
        if not REDIS_AVAILABLE:
            logger.info("Using in-memory fallback (redis not installed)")
            return
        
        try:
            self._redis = aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            # Test connection
            await self._redis.ping()
            logger.info(f"Connected to Redis: {self.redis_url}")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, using in-memory fallback")
            self._redis = None
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
    
    def _key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        if self._redis:
            return await self._redis.get(self._key(key))
        return self._memory_store.get(self._key(key))
    
    async def set(self, key: str, value: str, ttl: int = 86400) -> bool:
        """Set value with TTL (seconds)."""
        full_key = self._key(key)
        if self._redis:
            return await self._redis.setex(full_key, ttl, value)
        self._memory_store[full_key] = value
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete key."""
        if self._redis:
            return await self._redis.delete(self._key(key)) > 0
        return self._memory_store.pop(self._key(key), None) is not None
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if self._redis:
            return await self._redis.exists(self._key(key)) > 0
        return self._key(key) in self._memory_store
    
    async def get_json(self, key: str) -> Any:
        """Get JSON value."""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set_json(self, key: str, value: Any, ttl: int = 86400) -> bool:
        """Set JSON value."""
        return await self.set(key, json.dumps(value), ttl)


# Global instance
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """Dependency for FastAPI."""
    return redis_client
