import redis.asyncio as redis
from contextlib import asynccontextmanager

# This should ideally come from config, but for now, hardcoding for simplicity
REDIS_URL = "redis://localhost:6379/0"

@asynccontextmanager
async def get_redis_connection():
    """Provides an async Redis connection."""
    try:
        r = await redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        yield r
    finally:
        if 'r' in locals() and r:
            await r.close()

async def set_value(key: str, value: str, expire_seconds: int = None):
    async with get_redis_connection() as r:
        await r.set(key, value, ex=expire_seconds)

async def get_value(key: str):
    async with get_redis_connection() as r:
        return await r.get(key)

async def delete_key(key: str):
    async with get_redis_connection() as r:
        await r.delete(key)