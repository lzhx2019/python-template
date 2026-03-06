#!/usr/bin/env bash
# ============================================================
# 数据备份脚本：使用 pg_dump 导出 PostgreSQL 数据库
# 用法：bash ops/scripts/backup.sh [输出目录]
# ============================================================

set -euo pipefail

BACKUP_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="${DB_CONTAINER:-app-db}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_DB="${POSTGRES_DB:-app}"
BACKUP_FILE="$BACKUP_DIR/${POSTGRES_DB}-${TIMESTAMP}.sql.gz"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

echo "[信息] 正在备份 PostgreSQL 数据库 ($POSTGRES_DB)..."

# 使用容器内的 pg_dump 导出并压缩
docker exec "$DB_CONTAINER" \
    pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" \
    | gzip > "$BACKUP_FILE"

echo "[完成] 备份已保存到：$BACKUP_FILE"
ls -lh "$BACKUP_FILE"
