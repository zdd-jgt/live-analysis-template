from deepseek import IntentRecognizer
from typing import List, Dict

class IntentAnalysisEngine:
    """多层级意图识别引擎"""

    def __init__(self,
                 model_path: str = 'r1-intent',
                 faq_threshold: float = 0.85):
        self.model = IntentRecognizer.load(model_path)
        self.faq_threshold = faq_threshold

    def predict(self, text: str) -> Dict:
        """三级意图识别"""
        # 第一层：FAQ快速匹配
        faq_result = self._faq_match(text)
        if faq_result['confidence'] > self.faq_threshold:
            return faq_result

        # 第二层：语义解析
        semantic_result = self._semantic_parse(text)
        if semantic_result.get('requires_human'):
            return {
                "type": "transfer_human",
                "confidence": 1.0
            }

        # 第三层：深度学习模型
        return self.model.predict(text)

    def _faq_match(self, text: str) -> Dict:
        """强化学习优化的FAQ匹配"""
        # 此处接入预定义的FAQ知识库
        return self.model.faq_pipeline(text)

    def _semantic_parse(self, text: str) -> Dict:
        """语义解析（退款/物流等关键动作识别）"""
        # 使用规则引擎+NER模型组合实现
        return self.model.semantic_pipeline(text)
