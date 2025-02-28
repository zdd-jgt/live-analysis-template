from fastapi import APIRouter, WebSocket, Depends
from core.danmu_connector import BilibiliConnector, DouyinConnector
from core.nlp_engine.emotion import EmotionAnalysisEngine
from api.middleware.auth import validate_ws_token
import json

router = APIRouter()
emotion_engine = EmotionAnalysisEngine()

@router.websocket("/danmu/ws")
async def danmu_websocket(
    websocket: WebSocket,
    platform: str = 'bilibili',
    room_id: str = Depends(validate_ws_token)
):
    await websocket.accept()

    # 初始化连接器
    connector = {
        'bilibili': BilibiliConnector,
        'douyin': DouyinConnector
    }[platform](room_id)

    try:
        await connector.connect()
        async for danmu in connector.message_stream():
            # 实时情感分析
            emotion = emotion_engine.analyze_single(danmu['text'])

            # 构建响应数据
            response = {
                **danmu,
                "emotion": emotion['dominant_emotion'],
                "confidence": emotion['confidence']
            }

            await websocket.send_json(response)

    except Exception as e:
        await websocket.close(code=1011, reason=f"Server Error: {str(e)}")
    finally:
        connector.stop()
