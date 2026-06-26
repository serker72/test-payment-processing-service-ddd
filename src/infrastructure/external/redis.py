import redis.asyncio as aioredis
from idemptx.backend import AsyncRedisBackend

from src.infrastructure.config.settings import settings

async_redis_client = aioredis.Redis.from_url(settings.get_redis_url())
async_idemptx_backend = AsyncRedisBackend(async_redis_client)
