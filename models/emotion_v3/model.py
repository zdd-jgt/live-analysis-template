import torch
from transformers import AutoModel, AutoConfig
from typing import Dict

class EmotionModel:
    """情感分析模型封装"""

    _instance = None

    def __new__(cls, model_path: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_model(model_path)
        return cls._instance

    def init_model(self, model_path: str):
        # 加载配置文件
        config = AutoConfig.from_pretrained(model_path)

        # 动态加载模型权重
        self.model = AutoModel.from_pretrained(
            model_path,
            config=config,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def predict(self, text: str) -> Dict:
        """单条文本预测"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits.squeeze().cpu().numpy()
        return self._format_output(logits)

    def _format_output(self, logits: np.ndarray) -> Dict:
        """格式化输出结构"""
        return {
            label: float(score)
            for label, score in zip(
                self.config.emotion_labels,
                torch.softmax(torch.tensor(logits), dim=-1)
            )
        }
