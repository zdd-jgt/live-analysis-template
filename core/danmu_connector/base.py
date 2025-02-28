import abc
import json
from typing import Dict, Any
import websockets
from loguru import logger

class DanmuConnector(abc.ABC):
    """弹幕协议适配抽象基类"""

    def __init__(self, room_id: str):
        self.room_id = room_id
        self._stop_event = asyncio.Event()
        self.ws_client = None

    @abc.abstractmethod
    def _get_websocket_url(self) -> str:
        """获取平台特定WebSocket地址"""
        pass

    @abc.abstractmethod
    def _parse_message(self, raw_data: bytes) -> Dict[str, Any]:
        """解析平台原始协议"""
        pass

    async def connect(self):
        """建立WebSocket连接"""
        ws_url = self._get_websocket_url()
        try:
            self.ws_client = await websockets.connect(ws_url)
            logger.info(f"Connected to {self.__class__.__name__} room {self.room_id}")
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            raise

    async def message_stream(self):
        """生成消息流"""
        try:
            while not self._stop_event.is_set():
                raw_data = await self.ws_client.recv()
                parsed = self._parse_message(raw_data)
                if parsed:
                    yield parsed
        except websockets.ConnectionClosed:
            logger.warning("WebSocket connection closed")
        finally:
            await self.disconnect()

    async def disconnect(self):
        """关闭连接"""
        if self.ws_client:
            await self.ws_client.close()
            self.ws_client = None
            logger.info("Disconnected gracefully")

    def stop(self):
        """停止监听"""
        self._stop_event.set()
