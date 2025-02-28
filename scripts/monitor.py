import psutil
import requests
from prometheus_client import start_http_server, Gauge

# 定义监控指标
CPU_LOAD = Gauge('system_cpu_load', 'CPU负载百分比')
MEM_USAGE = Gauge('system_mem_usage', '内存使用量(MB)')
GPU_MEM = Gauge('gpu_memory_usage', 'GPU显存使用量(MB)', ['device_id'])

def collect_system_metrics():
    """收集主机资源指标"""
    # CPU
    CPU_LOAD.set(psutil.cpu_percent())

    # 内存
    mem = psutil.virtual_memory()
    MEM_USAGE.set(mem.used // 1024**2)

    # GPU
    try:
        import pynvml
        pynvml.nvmlInit()
        for i in range(pynvml.nvmlDeviceGetCount()):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            GPU_MEM.labels(device_id=str(i)).set(info.used // 1024**2)
    except ImportError:
        pass

if __name__ == "__main__":
    start_http_server(9100)
    while True:
        collect_system_metrics()
        time.sleep(5)
