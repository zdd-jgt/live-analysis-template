"""add analysis flag

Revision ID: 8a2b3c4d5e6f
Revises: 4c8a6e3f5c1a
Create Date: 2024-04-01 09:15:32.543210

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '8a2b3c4d5e6f'
down_revision = '4c8a6e3f5c1a'
branch_labels = None
depends_on = None

def upgrade():
    # 添加分析状态标记
    op.add_column(
        'danmu_records',
        sa.Column('analysis_status', sa.SmallInteger(),
                 nullable=False,
                 server_default='0',
                 comment='0=未分析 1=已分析 2=分析失败')
    )
    # 添加外部服务ID字段
    op.add_column(
        'danmu_records',
        sa.Column('external_id', sa.String(128),
                 unique=True,
                 comment='第三方平台原始ID')
    )

def downgrade():
    op.drop_column('danmu_records', 'analysis_status')
    op.drop_column('danmu_records', 'external_id')
