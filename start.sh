#!/bin/bash
# DeepSeek Live Analysis System Boot Script

set -euo pipefail
IFS=$'\n\t'

# 配置常量
DEFAULT_PORT=8000
LOG_DIR="./logs"
CONFIG_FILE="./config/settings.py"

# 环境检测
init_environment() {
    # 创建日志目录
    mkdir -p "${LOG_DIR}"

    # 检查Python版本
    if ! python3 -c 'import sys; assert sys.version_info >= (3,9)' >/dev/null 2>&1; then
        echo "错误：需要Python 3.9或更高版本"
        exit 1
    fi

    # 检查CUDA可用性
    if python3 -c 'import torch; print(torch.cuda.is_available())' | grep -q True; then
        echo "检测到CUDA加速可用"
        export CUDA_ENABLED=1
    else
        echo "警告：未检测到CUDA设备，使用CPU模式"
        export CUDA_ENABLED=0
    fi
}

# 数据库初始化
init_database() {
    if [ ! -f .db_initialized ]; then
        echo "正在初始化数据库..."
        python3 -m alembic upgrade head
        touch .db_initialized
    fi
}

# 启动API服务
start_api() {
    local mode=$1
    local workers=$(( $(nproc) * 2 + 1 ))

    case "${mode}" in
        dev)
            echo "启动开发服务器（热重载模式）..."
            uvicorn api.main:app \
                --host 0.0.0.0 \
                --port ${DEFAULT_PORT} \
                --reload \
                --reload-dir api \
                --reload-dir core \
                --log-level debug
            ;;
        prod)
            echo "启动生产服务器（${workers}工作进程）..."
            gunicorn api.main:app \
                -w ${workers} \
                -k uvicorn.workers.UvicornWorker \
                --bind 0.0.0.0:${DEFAULT_PORT} \
                --timeout 120 \
                --access-logfile - \
                --error-logfile - \
                --worker-tmp-dir /dev/shm
            ;;
        *)
            echo "未知模式: ${mode}"
            exit 1
            ;;
    esac
}

# 启动监控服务
start_monitor() {
    nohup python3 scripts/monitor.py >> "${LOG_DIR}/monitor.log" 2>&1 &
    echo "监控服务已启动（PID: $!）"
}

# 主流程
main() {
    init_environment
    init_database

    local mode=${1:-dev}
    shift

    case "${mode}" in
        dev|prod)
            start_api "${mode}"
            ;;
        monitor)
            start_monitor
            ;;
        test)
            pytest tests/ -v "$@"
            ;;
        migrate)
            alembic revision --autogenerate -m "$*"
            alembic upgrade head
            ;;
        *)
            echo "用法: $0 [模式]"
            echo "可用模式:"
            echo "  dev      - 开发模式（默认）"
            echo "  prod     - 生产模式"
            echo "  monitor  - 启动资源监控"
            echo "  test     - 运行测试套件"
            echo "  migrate  - 生成并执行迁移"
            exit 1
            ;;
    esac
}

# 执行入口
main "$@"
