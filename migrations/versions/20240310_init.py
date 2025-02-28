"""initial migration

Revision ID: 4c8a6e3f5c1a
Revises:
Create Date: 2024-03-10 15:32:45.215389

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '4c8a6e3f5c1a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 弹幕记录表
    op.create_table(
        'danmu_records',
        sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.String(64), index=True),
        sa.Column('platform', sa.String(32), nullable=False),
        sa.Column('emotion_scores', postgresql.JSONB),
        sa.Column('dominant_emotion', sa.String(32)),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )

    # 情绪统计表
    op.create_table(
        'sentiment_stats',
        sa.Column('time_bucket', sa.DateTime(timezone=True), primary_key=True),
        sa.Column('platform', sa.String(32), primary_key=True),
        sa.Column('joy_count', sa.Integer(), default=0),
        sa.Column('anger_count', sa.Integer(), default=0),
        sa.Column('sorrow_count', sa.Integer(), default=0),
        sa.Column('fear_count', sa.Integer(), default=0),
        sa.Column('surprise_count', sa.Integer(), default=0),
        sa.Column('disgust_count', sa.Integer(), default=0),
        sa.Column('neutral_count', sa.Integer(), default=0)
    )

    # 创建索引
    op.create_index('ix_danmu_timestamp', 'danmu_records', ['timestamp'])
    op.create_index('ix_sentiment_time', 'sentiment_stats', ['time_bucket'])

def downgrade():
    op.drop_table('sentiment_stats')
    op.drop_table('danmu_records')
