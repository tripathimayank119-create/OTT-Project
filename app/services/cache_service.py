from typing import Optional, List, Any
import redis.asyncio as redis


class CacheService:
    """Redis cache service for search results and popular content."""
    
    def __init__(self):
        self.redis_client = redis.from_url("redis://localhost:6379/0", decode_responses=True)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            val = await self.redis_client.get(key)
            if val is None:
                return None
            return val
        except Exception:
            return None
    
    async def set(
        self, key: str, value: Any, expire_seconds: int = 300
    ) -> bool:
        """Set value in cache with expiration."""
        try:
            await self.redis_client.set(key, str(value), ex=expire_seconds)
            return True
        except Exception:
            return False
    
    async def invalidate(self, key: str) -> bool:
        """Invalidate cache key."""
        try:
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False