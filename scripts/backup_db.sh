#!/bin/bash
# PostgreSQL数据库备份工具

TIMESTAMP=$(date +%Y%m%d%H%M)
BACKUP_DIR="/backups"
DB_NAME="live_analysis"

mkdir -p ${BACKUP_DIR}

# 执行备份
pg_dump -h ${DB_HOST} -U ${DB_USER} -Fc ${DB_NAME} > \
    ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.dump

# 加密备份文件
openssl enc -aes-256-cbc -salt -in ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.dump \
    -out ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.enc -pass pass:${ENCRYPT_KEY}

# 保留最近7天备份
find ${BACKUP_DIR} -name "*.enc" -type f -mtime +7 -exec rm {} \;
