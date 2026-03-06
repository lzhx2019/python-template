#!/usr/bin/env bash
# ============================================================
# 一键部署脚本：拉取最新代码并重新构建、启动所有服务
# 用法：bash ops/scripts/deploy.sh [--no-cache]
# ============================================================

set -euo pipefail

# 项目根目录（脚本所在位置向上两级）
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OPS_DIR="$PROJECT_ROOT/ops"

echo "=============================="
echo " 开始部署"
echo "=============================="

# 进入 ops 目录
cd "$OPS_DIR"

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "[警告] ops/.env 文件不存在，正在从模板复制..."
    cp .env.example .env
    echo "[提示] 请编辑 ops/.env 配置后重新运行此脚本"
    exit 1
fi

# 判断是否使用 --no-cache
BUILD_ARGS=""
if [[ "${1:-}" == "--no-cache" ]]; then
    BUILD_ARGS="--no-cache"
    echo "[信息] 构建将不使用缓存"
fi

# 拉取最新代码
echo "[1/4] 拉取最新代码..."
cd "$PROJECT_ROOT"
git pull --rebase

# 构建镜像
echo "[2/4] 构建 Docker 镜像..."
cd "$OPS_DIR"
docker compose -f docker-compose.yml build $BUILD_ARGS

# 停止旧容器
echo "[3/4] 停止旧容器..."
docker compose -f docker-compose.yml down

# 启动新容器
echo "[4/4] 启动新容器..."
docker compose -f docker-compose.yml up -d

echo ""
echo "=============================="
echo " 部署完成"
echo "=============================="
echo " 前端地址：http://localhost:${FRONTEND_PORT:-80}"
echo " 后端地址：http://localhost:${BACKEND_PORT:-8000}"
echo " API 文档：http://localhost:${BACKEND_PORT:-8000}/docs"
echo "=============================="

# 显示容器运行状态
docker compose -f docker-compose.yml ps
