import asyncpg
from contextlib import asynccontextmanager
from config import settings

class PostgresManager:
    """异步PostgreSQL连接池管理"""

    _pool = None

    @classmethod
    async def get_pool(cls):
        if not cls._pool:
            cls._pool = await asyncpg.create_pool(
                dsn=settings.PG_DSN,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
        return cls._pool

    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            yield conn

    @classmethod
    async def execute(cls, query: str, *args):
        async with cls.get_connection() as conn:
            return await conn.execute(query, *args)

    @classmethod
    async def fetch(cls, query: str, *args):
        async with cls.get_connection() as conn:
            return await conn.fetch(query, *args)
