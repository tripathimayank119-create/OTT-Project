
import json
import os
from typing import Any, Optional

from redis.asyncio import Redis


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

TITLE_CACHE_PATTERN = "titles:*"

redis_client: Optional[Redis] = None


async def get_redis():
    global redis_client

    if redis_client is None:
        redis_client = Redis.from_url(
            REDIS_URL,
            decode_responses=True,
        )

    return redis_client


async def cache_get(key: str) -> Optional[Any]:
    try:
        client = await get_redis()
        value = await client.get(key)

        if value is None:
            return None

        return json.loads(value)

    except Exception:
        return None


async def cache_set(
    key: str,
    value: Any,
    expiration: int = 300,
):
    try:
        client = await get_redis()

        await client.set(
            key,
            json.dumps(value),
            ex=expiration,
        )

    except Exception:
        pass


async def cache_delete(key: str):
    try:
        client = await get_redis()
        await client.delete(key)

    except Exception:
        pass


async def cache_clear():
    """Delete only this application's title-list cache entries."""
    try:
        client = await get_redis()
        keys = []

        async for key in client.scan_iter(
            match=TITLE_CACHE_PATTERN,
            count=100,
        ):
            keys.append(key)

            if len(keys) >= 100:
                await client.delete(*keys)
                keys.clear()

        if keys:
            await client.delete(*keys)

    except Exception:
        pass


async def close_redis():
    global redis_client

    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None
