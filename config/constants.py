from enum import Enum

class EmotionLabels(Enum):
    """情感分析标签枚举"""
    JOY = "joy"
    ANGER = "anger"
    SORROW = "sorrow"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"

# 平台常量
PLATFORMS = {
    "BILIBILI": "bilibili",
    "DOUYIN": "douyin"
}

# 错误消息
ERROR_MESSAGES = {
    "AUTH_FAILED": "Authentication failed",
    "RATE_LIMIT_EXCEEDED": "Too many requests",
    "PLATFORM_NOT_SUPPORTED": "Unsupported platform"
}

# HTTP状态码
HTTP_CODES = {
    "SUCCESS": 200,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "SERVER_ERROR": 500
}

# 情感阈值
THRESHOLDS = {
    "HIGH_CONFIDENCE": 0.85,
    "WARNING_LEVEL": 0.7,
    "MINIMAL_CONFIDENCE": 0.3
}

# 可视化参数
VISUALIZATION = {
    "HEATMAP_COLORS": ["#FF6B6B", "#4ECDC4"],
    "MAX_HISTORY_DAYS": 30
}

# 智能客服流程
CS_FLOW = {
    "MAX_RETRIES": 3,
    "TIMEOUT_SECONDS":
