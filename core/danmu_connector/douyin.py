import zlib
from .base import DanmuConnector

class DouyinConnector(DanmuConnector):
    """抖音弹幕协议解析"""

    def _get_websocket_url(self) -> str:
        return f"wss://webcast3-ws-web-hl.douyin.com/webcast/im/push/v2/?room_id={self.room_id}"

    def _parse_message(self, raw_data: bytes) -> dict:
        try:
            # 抖音协议解压与解析
            decompressed = zlib.decompress(raw_data[16:])
            data = json.loads(decompressed)

            if data.get('type') != 'comment':
                return None

            return {
                "user": data['user']['nickname'],
                "text": data['content'],
                "timestamp": data['timestamp'],
                "gift": data.get('gift_info'),
                "platform": "douyin"
            }
        except Exception as e:
            logger.error(f"抖音协议解析失败: {str(e)}")
            return None
