from deepseek import EmotionAnalyzer
import numpy as np
from typing import List, Dict

class EmotionAnalysisEngine:
    """七维情感分析引擎"""

    def __init__(self, model_path: str = 'r1-full'):
        self.model = EmotionAnalyzer.load(model_path)
        self.labels = ['joy', 'anger', 'sorrow', 'fear', 'surprise', 'disgust', 'neutral']

    def analyze_single(self, text: str) -> Dict[str, float]:
        """单条文本分析"""
        logits = self.model.forward(text)
        return self._format_output(logits)

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """批量分析（优化GPU利用率）"""
        batch_logits = self.model.batch_forward(texts)
        return [self._format_output(logits) for logits in batch_logits]

    def _format_output(self, logits: np.ndarray) -> Dict:
        """格式化输出结构"""
        scores = {label: float(score)
                 for label, score in zip(self.labels, logits)}
        dominant_idx = np.argmax(logits)
        return {
            "scores": scores,
            "dominant_emotion": self.labels[dominant_idx],
            "confidence": float(logits[dominant_idx])
        }
