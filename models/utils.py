import logging
from typing import List

def dynamic_batch(texts: List[str], max_tokens: int = 512) -> List[List[str]]:
    """动态批处理优化"""
    batches = []
    current_batch = []
    current_length = 0

    for text in texts:
        token_count = len(text) // 3  # 简易估算
        if current_length + token_count > max_tokens:
            batches.append(current_batch)
            current_batch = []
            current_length = 0

        current_batch.append(text)
        current_length += token_count

    if current_batch:
        batches.append(current_batch)

    return batches

def log_gpu_memory():
    """显存监控"""
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            alloc = torch.cuda.memory_allocated(i) // 1024**2
            total = torch.cuda.mem_get_info(i)[1] // 1024**2
            logging.info(f"GPU {i}: {alloc}MB / {total}MB used")
