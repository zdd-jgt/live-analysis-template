import os
from pydantic import BaseSettings, Field
from typing import Dict, Any

class Settings(BaseSettings):
    # 数据库配置
    PG_DSN: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/live_analysis",
        env="POSTGRES_DSN"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )

    # 安全配置
    JWT_SECRET: str = Field(
        default="your-secret-key-here",
        env="JWT_SECRET"
    )
    JWT_ALGORITHM: str = Field(default="HS256")
    TOKEN_EXPIRE_MINUTES: int = Field(default=1440)  # 24小时

    # 模型路径
    EMOTION_MODEL_PATH: str = Field(
        default="/models/emotion_v3",
        env="DEEPSEEK_MODEL_PATH"
    )

    # 速率限制配置
    RATE_LIMITS: Dict[str, Any] = Field(
        default={
            "global": {"requests": 1000, "seconds": 60},
            "per_ip": {"requests": 100, "seconds": 60}
        }
    )

    # 平台API密钥
    PLATFORM_KEYS: Dict[str, str] = Field(
        default={
            "bilibili": "your-bilibili-key",
            "douyin": "your-douyin-key"
        }
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
