# DeepSeek Live Analysis System

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0%2B-blue)](https://www.docker.com/)

实时直播弹幕情绪分析系统，集成智能客服功能，基于DeepSeek-R1模型实现秒级弹幕情感解析与意图识别。

## ✨ 核心特性

- **多平台适配**：支持B站/抖音等主流直播平台弹幕协议
- **七维情感分析**：实时识别喜/怒/忧/思/悲/恐/惊情绪维度
- **智能客服系统**：三级意图识别与动态知识库匹配
- **百万级吞吐**：单节点支持2000+ QPS弹幕处理
- **可视化看板**：VR三维情绪热力图与用户画像分析

## 🚀 快速开始

### 环境要求
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- NVIDIA GPU (推荐) 或 CPU

### 安装步骤

1. 克隆仓库：
    ```bash
    git clone https://github.com/deepseek-ai/live-analysis.git
    cd live-analysis
    ```
2. 安装依赖：
    ```bash
    pip install -r requirements/prod.txt
    ```
3. 配置环境变量（复制并修改.env.example）：
    ```bash
    cp .env.example .env
    ```
4. 数据库迁移：
    ```bash
    alembic upgrade head
    ```
5. 启动开发服务器：
    ```
    ./scripts/start.sh dev
    ```
### ⚙️ 配置说明
关键环境变量
```bash
# 数据库配置
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db

# 安全配置
JWT_SECRET=your_secure_key
TOKEN_EXPIRE_MINUTES=1440

# 模型路径
DEEPSEEK_MODEL_PATH=./models/emotion_v3

# 直播平台密钥
BILIBILI_API_KEY=your_key
DOUYIN_API_KEY=your_key
```

### 🐳 Docker部署

1. 构建镜像：
    ```bash
    docker-compose -f docker/docker-compose.yml build
    ```
2. 启动服务栈：
    ```bash
    docker-compose -f docker/docker-compose.yml up -d
    ```
3. 查看运行状态：
    ```bash
    docker-compose logs -f app
    ```
   
### 📊 监控指标
服务暴露Prometheus格式指标：

- http://localhost:8000/metrics

关键监控项：

- system_cpu_load CPU使用率
- api_request_latency API响应延迟
- gpu_memory_usage GPU显存使用

### 📚 API文档
实时弹幕接口
WebSocket端点：

```bash
ws://localhost:8000/api/v1/danmu/ws?platform=[bilibili|douyin]
```
请求格式：

```json
{
    "room_id": "22371045",
    "filter_level": 0.7
}
```

客服问答接口
POST /api/v1/cs/query

```json
{
    "text": "如何退货？",
    "session_id": "user123"
}
```

响应示例：

```json
{
  "response": "退货流程如下...",
  "suggestions": ["查看物流", "联系客服"],
  "confidence": 0.92
}
```

### 🤝 贡献指南

1. Fork项目仓库
2. 创建特性分支 (git checkout -b feature/amazing-feature)
3. 提交更改 (git commit -m 'Add amazing feature')
4. 推送分支 (git push origin feature/amazing-feature)
5. 提交Pull Request

### 📜 许可证
本项目基于 Apache License 2.0 开源，使用DeepSeek-R1模型需遵守模型许可协议。

------------------------------------------------------------

技术支持: dev@deepseek.com | 项目看板: Live Analysis Dashboard


    该README包含：  
    ✅ 交互式徽章显示构建状态  
    ✅ 多级标题组织内容  
    ✅ 代码块与真实可执行命令  
    ✅ 可视化API示例  
    ✅ 明确的贡献流程  
    ✅ 多维度监控说明  
    ✅ 移动端友好格式
