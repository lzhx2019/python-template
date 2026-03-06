#!/usr/bin/env bash
# ============================================================
# 健康检查脚本：检测前后端服务是否正常运行
# 用法：bash ops/scripts/health-check.sh
# 可配合 cron 定时任务使用
# ============================================================

set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000/health}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:80}"

check_service() {
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

echo "=============================="
echo " 服务健康检查"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================="

FAILED=0

check_service "后端 API" "$BACKEND_URL" || FAILED=1
check_service "前端页面" "$FRONTEND_URL" || FAILED=1

echo "=============================="

if [ "$FAILED" -eq 1 ]; then
    echo "[结果] 存在异常服务，请检查！"
    exit 1
else
    echo "[结果] 所有服务运行正常"
    exit 0
fi
