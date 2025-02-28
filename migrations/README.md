使用说明
初始化迁移环境
alembic init migrations
创建新迁移脚本
alembic revision -m "add new features" --autogenerate
执行迁移
# 应用所有迁移
alembic upgrade head

# 回滚到指定版本
alembic downgrade 4c8a6e3f5c1a
环境变量配置（.env文件）
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=live_analysis

关键特性
异步数据库支持
# env.py中配置异步引擎
async def run_async_migrations():
engine = create_async_engine(settings.PG_DSN)
async with engine.connect() as conn:
await conn.run_sync(do_run_migrations)
JSONB字段存储情感分数
sa.Column('emotion_scores', postgresql.JSONB)  # 存储七维情感得分
复合主键设计
# 情绪统计表使用时间+平台作为复合主键
sa.Column('time_bucket', sa.DateTime, primary_key=True),
sa.Column('platform', sa.String(32), primary_key=True)
自动生成迁移脚本
# 模型变更后自动检测差异
alembic revision --autogenerate -m "description"
该迁移系统支持：

自动检测模型变更生成迁移脚本
异步数据库操作
多平台数据分片存储
细粒度统计字段设计
生产环境安全回滚机制
