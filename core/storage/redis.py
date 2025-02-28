import aioredis
from config import settings

class RedisManager:
    """Redis连接管理器"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.redis = None
        return cls._instance

    async def initialize(self):
        if not self.redis:
            self.redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )

    async def set(self, key: str, value: str, ttl: int = 3600):
        await self.redis.set(key, value, ex=ttl)

    async def get(self, key: str) -> str:
        return await self.redis.get(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
