#!/bin/bash

# 等待数据库就绪
function wait_for_db() {
    until pg_isready -h postgres -U ${DB_USER} -d ${DB_NAME}; do
        echo "Waiting for PostgreSQL..."
        sleep 2
    done
}

# 执行数据库迁移
function run_migrations() {
    echo "Running database migrations..."
    alembic upgrade head
}

# 主启动流程
function main() {
    wait_for_db
    run_migrations

    # 根据环境变量选择运行模式
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "Starting production server..."
        gunicorn api.main:app \
            --workers 4 \
            --worker-class uvicorn.workers.UvicornWorker \
            --bind 0.0.0.0:8000 \
            --timeout 120 \
            --access-logfile -
    else
        echo "Starting development server..."
        uvicorn api.main:app \
            --host 0.0.0.0 \
            --port 8000 \
            --reload \
            --reload-dir /app \
            --log-level debug
    fi
}

main
