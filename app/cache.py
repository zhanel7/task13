import redis.asyncio as redis
import json
from typing import Optional

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_cached_notes(key: str) -> Optional[list]:
    cached = await r.get(key)
    if cached:
        return json.loads(cached)
    return None

async def set_cached_notes(key: str, data: list, ttl: int = 600):
    await r.set(key, json.dumps(data), ex=ttl)

async def invalidate_notes_cache(prefix: str):
    keys = await r.keys(f"{prefix}*")
    if keys:
        await r.delete(*keys)
