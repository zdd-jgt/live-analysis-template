from fastapi import Request, HTTPException
from core.storage.redis import RedisManager
from config.settings import RATE_LIMIT
import asyncio

class RateLimiter:
    def __init__(self):
        self.redis = RedisManager()

    async def check_limit(self, key: str, limit: int, period: int):
        """滑动窗口限流算法"""
        current = int(time.time())
        window_start = current - period

        pipe = await self.redis.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zcard(key)
        pipe.zadd(key, {current: current})
        pipe.expire(key, period)
        results = await pipe.execute()

        if results[1] >= limit:
            raise HTTPException(status_code=429, detail="Too many requests")

async def rate_limiter_middleware(request: Request, call_next):
    """全局限流中间件"""
    limiter = RateLimiter()
    client_ip = request.client.host
    path = request.url.path

    # 双层级限流
    await limiter.check_limit(
        f"global:{path}",
        RATE_LIMIT['global']['limit'],
        RATE_LIMIT['global']['period']
    )

    await limiter.check_limit(
        f"ip:{client_ip}:{path}",
        RATE_LIMIT['per_ip']['limit'],
        RATE_LIMIT['per_ip']['period']
    )

    response = await call_next(request)
    return response
