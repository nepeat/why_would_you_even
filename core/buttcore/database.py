import os
import asyncio_redis

async def get_redis():
    return await asyncio_redis.Connection.create(
        host=os.environ.get("REDIS_HOST", "127.0.0.1"),
        port=os.environ.get("REDIS_PORT", 6379),
        db=os.environ.get("REDIS_DB", 0),
        encoder=asyncio_redis.encoders.UTF8Encoder()
    )
