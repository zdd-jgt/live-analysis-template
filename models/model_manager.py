import hashlib
from pathlib import Path
from fastapi import BackgroundTasks
from deepseek.utils import download_model

class ModelManager:
    """模型动态加载与缓存管理"""

    def __init__(self):
        self.loaded_models = {}
        self.model_dir = Path("models")

    async def get_model(self, model_name: str, bg_tasks: BackgroundTasks):
        """获取模型实例（按需加载）"""
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        model_path = self.model_dir / model_name
        if not model_path.exists():
            # 触发异步下载任务
            bg_tasks.add_task(
                self._download_model,
                model_name,
                model_path
            )
            raise ModelNotReadyError()

        model = EmotionModel(str(model_path))
        self.loaded_models[model_name] = model
        return model

    async def _download_model(self, name: str, path: Path):
        """模型下载与校验"""
        tmp_path = path.with_suffix(".tmp")
        await download_model(
            repo_id=f"deepseek/{name}",
            local_dir=tmp_path
        )

        # 完整性校验
        if self._verify_model(tmp_path):
            tmp_path.rename(path)

    def _verify_model(self, path: Path) -> bool:
        """SHA256校验"""
        expected_hash = {
            "emotion_v3": "a1b2c3d4e5f6..."
        }.get(path.name)

        sha256 = hashlib.sha256()
        with open(path/"pytorch_model.bin", "rb") as f:
            while chunk := f.read(1024 * 1024):
                sha256.update(chunk)

        return sha256.hexdigest() == expected_hash
