安装说明
基础环境安装：

pip install -r requirements/base.txt
开发环境安装：

pip install -r requirements/dev.txt
生产环境安装：

pip install -r requirements/prod.txt
版本锁定策略
深度学习框架
明确指定CUDA版本：

torch==1.12.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
安全组件
锁定加密库版本：

cryptography==3.4.8  # 已知稳定版本
运行时依赖
生产环境锁定核心组件：

fastapi==0.68.0
uvicorn==0.15.0
关键依赖说明
GPU加速支持

torch==1.12.0+cu113  # 明确CUDA 11.3版本
bitsandbytes>=0.37.0  # 8bit量化支持
异步IO优化

uvloop>=0.16.0  # 替代asyncio事件循环
安全加固组件

python-jose[cryptography]  # JWT标准实现
passlib[bcrypt]  # 密码哈希算法
监控告警系统

prometheus-client  # 暴露监控指标
sentry-sdk  # 错误日志收集
该配置方案具有以下特点：

环境隔离：通过分层依赖管理实现开发/生产环境隔离
版本控制：核心组件在生产环境锁定版本
硬件适配：明确指定CUDA版本避免兼容性问题
安全加固：独立的安全组件版本控制
性能优化：包含uvloop、orjson等加速库
建议结合pyproject.toml使用现代Python打包标准：


[project]
dependencies = [
"fastapi>=0.68.0",
"uvicorn[standard]>=0.15.0",
"deepseek-sdk>=2.4.0"
]

[project.optional-dependencies]
dev = [
"pytest>=7.0.0",
"black>=22.3.0"
]
prod = [
"gunicorn>=20.1.0",
"uvloop>=0.16.0"
]
