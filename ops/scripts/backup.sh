#!/usr/bin/env bash
# ============================================================
# 数据备份脚本：导出后端数据卷到 tar 归档
# 用法：bash ops/scripts/backup.sh [输出目录]
# ============================================================

set -euo pipefail

BACKUP_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backend-data-$TIMESTAMP.tar.gz"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

echo "[信息] 正在备份后端数据卷..."

# 使用临时容器挂载数据卷并打包
docker run --rm \
    -v ops_backend-data:/data \
    -v "$BACKUP_DIR":/backup \
    alpine \
    tar czf "/backup/backend-data-$TIMESTAMP.tar.gz" -C /data .

echo "[完成] 备份已保存到：$BACKUP_FILE"
ls -lh "$BACKUP_FILE"
