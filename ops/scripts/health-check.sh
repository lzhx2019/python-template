#!/usr/bin/env bash
# ============================================================
# 健康检查脚本：检测 PostgreSQL、后端、前端服务是否正常运行
# 用法：bash ops/scripts/health-check.sh
# 可配合 cron 定时任务使用
# ============================================================

set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000/health}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:80}"
DB_CONTAINER="${DB_CONTAINER:-app-db}"

check_http() {
    local name="$1"
    local url="$2"
    local status

    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")

    if [ "$status" = "200" ]; then
        echo "[正常] $name ($url) - HTTP $status"
        return 0
    else
        echo "[异常] $name ($url) - HTTP $status"
        return 1
    fi
}

check_postgres() {
    local name="PostgreSQL"
    if docker exec "$DB_CONTAINER" pg_isready -U postgres > /dev/null 2>&1; then
        echo "[正常] $name ($DB_CONTAINER) - 接受连接"
        return 0
    else
        echo "[异常] $name ($DB_CONTAINER) - 无法连接"
        return 1
    fi
}

echo "=============================="
echo " 服务健康检查"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================="

FAILED=0

check_postgres    || FAILED=1
check_http "后端 API" "$BACKEND_URL" || FAILED=1
check_http "前端页面" "$FRONTEND_URL" || FAILED=1

echo "=============================="

if [ "$FAILED" -eq 1 ]; then
    echo "[结果] 存在异常服务，请检查！"
    exit 1
else
    echo "[结果] 所有服务运行正常"
    exit 0
fi
