import xml.etree.ElementTree as ET
from .base import DanmuConnector

class BilibiliConnector(DanmuConnector):
    """B站弹幕协议解析"""

    def _get_websocket_url(self) -> str:
        return f"wss://broadcastlv.chat.bilibili.com/sub?room_id={self.room_id}"

    def _parse_message(self, raw_data: bytes) -> dict:
        try:
            # B站协议解析逻辑
            root = ET.fromstring(raw_data.decode('utf-8'))
            msg_type = root.find('.//type').text
            if msg_type != 'danmaku':
                return None

            return {
                "user": root.find('.//nickname').text,
                "text": root.find('.//content').text,
                "timestamp": int(root.find('.//timestamp').text),
                "color": root.find('.//color').text,
                "platform": "bilibili"
            }
        except Exception as e:
            logger.error(f"B站协议解析失败: {str(e)}")
            return None
