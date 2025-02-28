#!/bin/bash
# 生产环境滚动更新部署脚本

set -euo pipefail

ENV=${1:-"prod"}
MODEL_VERSION=${2:-"r1-full-v3"}

# 加载环境变量
source ../config/.env.${ENV}

# 执行滚动更新
docker-compose -f ../docker/docker-compose.prod.yml build --build-arg MODEL_VERSION=${MODEL_VERSION}
docker-compose -f ../docker/docker-compose.prod.yml up -d --scale app=3 --no-deps --wait

# 健康检查
HEALTH_CHECK_URL="http://${SERVER_IP}:8000/health"
for i in {1..10}; do
    if curl -s --fail ${HEALTH_CHECK_URL}; then
        echo "Health check passed"
        break
    else
        sleep 10
        echo "Retrying health check..."
    fi
done

# 清理旧容器
docker system prune -af --filter "label=com.deepseek.version!=${MODEL_VERSION}"

echo "Deployment completed successfully"
