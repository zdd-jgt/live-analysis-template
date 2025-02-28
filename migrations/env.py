import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from core.storage.postgres import Base  # 导入模型基类
from config.settings import settings

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        version_table="alembic_version",
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine(settings.PG_DSN)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    raise Exception("Async migrations require online mode")
else:
    run_migrations_online()
