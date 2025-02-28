from fastapi import APIRouter, Body, HTTPException
from core.nlp_engine.intent import IntentAnalysisEngine
from pydantic import BaseModel
import logging

router = APIRouter()
intent_engine = IntentAnalysisEngine()

class CustomerRequest(BaseModel):
    text: str
    session_id: str
    user_id: str = 'anonymous'

@router.post("/customer_service/query")
async def handle_customer_query(
    request: CustomerRequest = Body(...)
):
    try:
        # 执行三级意图识别
        intent_result = intent_engine.predict(request.text)

        # 敏感词过滤
        if contains_sensitive_words(request.text):
            return {"action": "block", "reason": "sensitive_content"}

        return {
            "session_id": request.session_id,
            "response": build_response(intent_result),
            "suggestions": generate_quick_replies(intent_result)
        }

    except Exception as e:
        logging.error(f"Query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def build_response(intent: dict) -> str:
    """构建响应内容"""
    if intent['type'] == 'faq':
        return intent['answer']
    elif intent['type'] == 'transaction':
        return f"正在为您处理{intent['action']}请求..."
    else:
        return "您的问题已转接人工客服，请稍候"

def generate_quick_replies(intent: dict) -> list:
    """生成快捷回复选项"""
    if intent['type'] == 'faq':
        return ["查看更多", "联系人工"]
    return []
