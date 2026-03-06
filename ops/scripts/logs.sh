#!/usr/bin/env bash
# ============================================================
# 查看服务日志
# 用法：bash ops/scripts/logs.sh [服务名] [行数]
#   服务名：backend / frontend，留空查看所有
#   行数：显示最近 N 行，默认 100
# ============================================================

set -euo pipefail

OPS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$OPS_DIR"

SERVICE="${1:-}"
LINES="${2:-100}"

if [ -n "$SERVICE" ]; then
    echo "[信息] 查看 $SERVICE 最近 $LINES 行日志..."
    docker compose -f docker-compose.yml logs --tail "$LINES" -f "$SERVICE"
else
    echo "[信息] 查看所有服务最近 $LINES 行日志..."
    docker compose -f docker-compose.yml logs --tail "$LINES" -f
fi
