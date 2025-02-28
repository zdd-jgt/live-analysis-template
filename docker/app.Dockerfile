# 基础镜像（使用DeepSeek官方优化镜像）
FROM deepseek/r1-inference:2.4.1-cuda11.8

# 设置清华镜像源
RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//mirror:\/\/mirrors.ubuntu.com\/mirrors.txt/' /etc/apt/sources.list && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app
COPY requirements.txt .

# 安装Python依赖（分离核心包与开发包）
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install "uvicorn[standard]" gunicorn==21.2.0

# 复制应用代码
COPY . .

# 配置模型存储路径
ENV DEEPSEEK_MODEL_PATH=/app/models
VOLUME /app/models

# 设置非root用户
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
ENTRYPOINT ["/app/docker/entrypoint.sh"]
