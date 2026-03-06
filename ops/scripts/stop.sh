#!/usr/bin/env bash
# ============================================================
# 停止所有服务
# 用法：bash ops/scripts/stop.sh [--clean]
#   --clean  停止并删除容器、网络和数据卷
# ============================================================

set -euo pipefail

OPS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$OPS_DIR"

if [[ "${1:-}" == "--clean" ]]; then
    echo "[信息] 停止服务并清除所有数据卷..."
    docker compose -f docker-compose.yml down -v
else
    echo "[信息] 停止服务（保留数据卷）..."
    docker compose -f docker-compose.yml down
fi

echo "[完成] 所有服务已停止"
