import asyncio
from datetime import timedelta
from sqlalchemy import select
from tqdm import tqdm
from core.storage.postgres import PostgresManager
from core.storage.redis import RedisManager

async def migrate_legacy_data(batch_size=1000):
    """从旧系统迁移数据到新数据库"""
    # 旧数据库连接
    old_conn = await asyncpg.connect(OLD_DB_DSN)

    # 分页迁移
    offset = 0
    while True:
        rows = await old_conn.fetch(
            "SELECT * FROM legacy_danmu LIMIT $1 OFFSET $2",
            batch_size, offset
        )
        if not rows:
            break

        # 转换数据结构
        transformed = [{
            "content": r["content"],
            "user_id": r["user_id"],
            "timestamp": r["created_at"],
            "metadata": {
                "old_id": r["id"],
                "platform": "legacy"
            }
        } for r in rows]

        # 批量写入新数据库
        async with PostgresManager.get_connection() as conn:
            await conn.executemany(
                "INSERT INTO danmu_records (content, user_id, timestamp, metadata) "
                "VALUES ($1, $2, $3, $4)",
                [(t["content"], t["user_id"], t["timestamp"], t["metadata"])
                 for t in transformed]
            )

        # 更新进度到Redis
        await RedisManager().set(
            "migration_progress",
            f"{offset + len(rows)} records migrated"
        )

        offset += batch_size

if __name__ == "__main__":
    asyncio.run(migrate_legacy_data())
