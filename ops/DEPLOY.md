# 部署与运维文档

本文档覆盖项目的容器化构建、部署流程、日常运维操作和故障排查。

---

## 目录

1. [ops 目录结构](#1-ops-目录结构)
2. [环境要求](#2-环境要求)
3. [快速部署](#3-快速部署)
4. [Docker 镜像说明](#4-docker-镜像说明)
5. [环境变量配置](#5-环境变量配置)
6. [部署方式](#6-部署方式)
7. [日常运维操作](#7-日常运维操作)
8. [监控与健康检查](#8-监控与健康检查)
9. [数据备份与恢复](#9-数据备份与恢复)
10. [日志管理](#10-日志管理)
11. [性能调优](#11-性能调优)
12. [安全加固](#12-安全加固)
13. [故障排查](#13-故障排查)
14. [CI/CD 集成参考](#14-cicd-集成参考)

---

## 1. ops 目录结构

```
ops/
├── Dockerfile.backend       # 后端镜像构建文件
├── Dockerfile.frontend      # 前端镜像构建文件（含 Nginx）
├── docker-compose.yml       # 生产环境编排
├── docker-compose.dev.yml   # 开发环境编排（挂载源码 + 热重载）
├── .env.example             # 环境变量模板
├── .gitignore               # 忽略 .env 等敏感文件
├── nginx/
│   └── nginx.conf           # Nginx 站点配置（SPA 路由 + API 反代）
├── scripts/
│   ├── deploy.sh            # 一键部署脚本
│   ├── stop.sh              # 停止服务脚本
│   ├── logs.sh              # 查看日志脚本
│   ├── backup.sh            # 数据备份脚本
│   └── health-check.sh      # 健康检查脚本
└── DEPLOY.md                # 本文档
```

---

## 2. 环境要求

| 工具 | 最低版本 | 说明 |
| ---- | -------- | ---- |
| Docker | >= 24.0 | 容器运行时 |
| Docker Compose | >= 2.20 | 多容器编排（Docker Desktop 自带）|
| Git | >= 2.30 | 代码管理 |

验证安装：

```bash
docker --version
docker compose version
```

---

## 3. 快速部署

适用于首次部署或快速搭建演示环境。

```bash
# 1. 克隆仓库
git clone <仓库地址>
cd <项目目录>

# 2. 准备环境变量
cp ops/.env.example ops/.env
# 编辑 ops/.env，修改 SECRET_KEY 等配置

# 3. 一键构建并启动
bash ops/scripts/deploy.sh
```

部署完成后：

| 服务 | 地址 |
| ---- | ---- |
| 前端页面 | http://localhost |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

---

## 4. Docker 镜像说明

### 4.1 后端镜像（`Dockerfile.backend`）

```
构建流程：
python:3.12-slim ──→ uv sync 安装依赖 ──→ 复制源码 ──→ uvicorn 启动
```

- **基础镜像**：`python:3.12-slim`（约 150MB）
- **包管理**：使用 uv 安装生产依赖，不包含开发依赖
- **运行命令**：`uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **健康检查**：每 30 秒请求 `/health` 接口

### 4.2 前端镜像（`Dockerfile.frontend`）

```
构建流程：
node:18-alpine ──→ npm ci ──→ npm run build ──→ nginx:1.27-alpine 托管 dist/
```

- **构建阶段**：Node 18 编译 TypeScript + Vite 打包
- **运行阶段**：Nginx Alpine（约 40MB）托管静态文件
- **Nginx 功能**：SPA 路由回退、API 反向代理、Gzip 压缩、安全响应头

### 4.3 手动构建镜像

```bash
# 在项目根目录执行

# 构建后端镜像
docker build -f ops/Dockerfile.backend -t app-backend:latest .

# 构建前端镜像
docker build -f ops/Dockerfile.frontend -t app-frontend:latest .
```

---

## 5. 环境变量配置

所有环境变量在 `ops/.env` 中配置（从 `.env.example` 复制）。

| 变量 | 说明 | 默认值 | 生产建议 |
| ---- | ---- | ------ | -------- |
| `POSTGRES_USER` | PostgreSQL 用户名 | `postgres` | 使用专用用户 |
| `POSTGRES_PASSWORD` | PostgreSQL 密码 | `postgres` | 使用强密码 |
| `POSTGRES_DB` | PostgreSQL 数据库名 | `app` | 按项目命名 |
| `DATABASE_URL` | 数据库连接字符串 | `postgresql://postgres:postgres@db:5432/app` | 与上方保持一致 |
| `DB_POOL_SIZE` | 数据库连接池大小 | `5` | 按并发量调整 |
| `DB_MAX_OVERFLOW` | 连接池最大溢出 | `10` | 按并发量调整 |
| `SECRET_KEY` | JWT 签名密钥 | `please-change-this...` | 随机 64 位字符串 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 令牌有效期（分钟） | `1440` | 按需调整 |
| `CORS_ORIGINS` | 允许跨域的来源 | `["http://localhost"]` | 设为实际域名 |
| `BACKEND_PORT` | 后端映射端口 | `8000` | 按需调整 |
| `FRONTEND_PORT` | 前端映射端口 | `80` | 按需调整 |
| `POSTGRES_PORT` | PostgreSQL 映射端口 | `5432` | 生产环境可不暴露 |

### 生成随机 SECRET_KEY

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
# 或
openssl rand -base64 48
```

---

## 6. 部署方式

### 6.1 Docker Compose 生产部署

```bash
cd ops

# 构建并启动（后台运行）
docker compose -f docker-compose.yml up -d --build

# 查看运行状态
docker compose -f docker-compose.yml ps

# 仅重启某个服务
docker compose -f docker-compose.yml restart backend
```

### 6.2 Docker Compose 开发部署

开发模式会挂载源码目录，支持热重载：

```bash
cd ops

# 启动开发环境
docker compose -f docker-compose.dev.yml up --build

# 后端修改 Python 代码后自动重载
# 前端修改 TSX/Less 后自动 HMR
```

### 6.3 数据库说明

项目默认使用 **PostgreSQL 16**，已集成在 `docker-compose.yml` 和 `docker-compose.dev.yml` 中。后端通过 `psycopg2-binary` 驱动连接，并配置了连接池。

Compose 启动时会自动：
1. 拉取 `postgres:16-alpine` 镜像并启动数据库容器
2. 后端等待数据库健康检查通过后再启动
3. 应用启动时自动创建所有表（通过 SQLModel `create_all`）

#### 使用外部 PostgreSQL

如果已有独立的 PostgreSQL 实例，可移除 Compose 中的 `db` 服务，仅修改 `ops/.env`：

```
DATABASE_URL=postgresql://user:password@your-db-host:5432/mydb
```

#### 连接池调优

在 `ops/.env` 中调整：

```
DB_POOL_SIZE=10        # 连接池常驻连接数
DB_MAX_OVERFLOW=20     # 超出 pool_size 后允许的最大临时连接数
```

#### 本地开发使用 SQLite

如不想安装 PostgreSQL，后端仍兼容 SQLite，修改 `backend/.env`：

```
DATABASE_URL=sqlite:///./app.db
```

---

## 7. 日常运维操作

### 7.1 一键部署/更新

```bash
bash ops/scripts/deploy.sh            # 常规部署
bash ops/scripts/deploy.sh --no-cache # 不使用缓存重新构建
```

### 7.2 停止服务

```bash
bash ops/scripts/stop.sh              # 停止（保留数据）
bash ops/scripts/stop.sh --clean      # 停止并清除数据卷
```

### 7.3 重启单个服务

```bash
cd ops
docker compose -f docker-compose.yml restart backend   # 重启后端
docker compose -f docker-compose.yml restart frontend   # 重启前端
```

### 7.4 查看容器资源占用

```bash
docker stats app-db app-backend app-frontend
```

### 7.5 进入容器内部调试

```bash
# 进入后端容器
docker exec -it app-backend bash

# 进入前端容器（Alpine 使用 sh）
docker exec -it app-frontend sh

# 进入数据库容器并连接 psql
docker exec -it app-db psql -U postgres -d app
```

---

## 8. 监控与健康检查

### 8.1 手动检查

```bash
bash ops/scripts/health-check.sh
```

输出示例：

```
==============================
 服务健康检查
 2026-03-06 12:00:00
==============================
[正常] PostgreSQL (app-db) - 接受连接
[正常] 后端 API (http://localhost:8000/health) - HTTP 200
[正常] 前端页面 (http://localhost:80) - HTTP 200
==============================
[结果] 所有服务运行正常
```

### 8.2 Docker 内置健康检查

两个容器均配置了 `HEALTHCHECK`，Docker 会自动检测：

```bash
docker inspect --format='{{.State.Health.Status}}' app-backend
docker inspect --format='{{.State.Health.Status}}' app-frontend
```

### 8.3 配合 Cron 定时检查

```bash
# 每 5 分钟执行一次健康检查，异常时发送告警
*/5 * * * * /path/to/ops/scripts/health-check.sh >> /var/log/health-check.log 2>&1 || mail -s "服务异常告警" admin@example.com < /var/log/health-check.log
```

---

## 9. 数据备份与恢复

备份脚本使用 `pg_dump` 导出 PostgreSQL 数据库为 SQL 压缩文件。

### 9.1 备份

```bash
bash ops/scripts/backup.sh                    # 备份到默认目录 backups/
bash ops/scripts/backup.sh /path/to/backup    # 备份到指定目录
```

生成文件格式：`app-20260306_120000.sql.gz`

### 9.2 恢复

```bash
# 解压并导入到数据库
gunzip -c backups/app-20260306_120000.sql.gz | docker exec -i app-db psql -U postgres -d app
```

如需恢复到干净数据库：

```bash
# 删除并重建数据库
docker exec app-db psql -U postgres -c "DROP DATABASE IF EXISTS app;"
docker exec app-db psql -U postgres -c "CREATE DATABASE app;"

# 导入备份
gunzip -c backups/app-20260306_120000.sql.gz | docker exec -i app-db psql -U postgres -d app

# 重启后端以重新建立连接
cd ops && docker compose -f docker-compose.yml restart backend
```

### 9.3 定时备份（Cron）

```bash
# 每天凌晨 3 点备份，保留最近 30 天
0 3 * * * /path/to/ops/scripts/backup.sh /data/backups && find /data/backups -name "*.sql.gz" -mtime +30 -delete
```

---

## 10. 日志管理

### 10.1 查看日志

```bash
bash ops/scripts/logs.sh                  # 所有服务，最近 100 行
bash ops/scripts/logs.sh backend          # 仅后端
bash ops/scripts/logs.sh frontend 200     # 前端，最近 200 行
```

### 10.2 直接使用 Docker 命令

```bash
# 实时跟踪后端日志
docker logs -f app-backend

# 查看指定时间段日志
docker logs --since 2026-03-06T00:00:00 --until 2026-03-06T12:00:00 app-backend
```

### 10.3 日志轮转

Docker 默认 JSON 日志驱动无限增长。建议在 `/etc/docker/daemon.json` 中配置：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  }
}
```

修改后重启 Docker：`sudo systemctl restart docker`

---

## 11. 性能调优

### 11.1 Uvicorn 多 Worker

生产环境建议使用多个 Worker 进程提升并发：

修改 `docker-compose.yml` 中 backend 的启动命令：

```yaml
command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Worker 数量建议：`CPU 核心数 * 2 + 1`

### 11.2 Nginx 缓存

Nginx 配置中已对 `/assets/` 目录设置了 1 年长期缓存（Vite 构建的文件名含 hash，内容变化时文件名会改变）。

### 11.3 Gzip 压缩

Nginx 配置中已启用 Gzip，覆盖 HTML、CSS、JS、JSON、SVG 等常见类型。

---

## 12. 安全加固

### 12.1 部署前必做

- [ ] 修改 `SECRET_KEY` 为随机强密码
- [ ] 修改 `POSTGRES_PASSWORD` 为强密码，并同步更新 `DATABASE_URL`
- [ ] `CORS_ORIGINS` 设置为实际域名，不要使用 `*`
- [ ] 生产环境不要暴露后端端口和 PostgreSQL 端口（仅容器内部访问）
- [ ] 配置 HTTPS（见下方说明）

### 12.2 配置 HTTPS

推荐使用 Let's Encrypt + Certbot。在 `ops/nginx/nginx.conf` 中添加 SSL 配置：

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # ... 其余配置不变
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}
```

在 `docker-compose.yml` 的 frontend 服务中挂载证书目录：

```yaml
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
ports:
  - "80:80"
  - "443:443"
```

### 12.3 隐藏后端端口

生产环境中，后端仅需被前端 Nginx 容器访问，无需映射到宿主机：

```yaml
backend:
  # 移除 ports 配置，仅在 Docker 内部网络暴露
  expose:
    - "8000"
```

---

## 13. 故障排查

### 问题：容器启动失败

```bash
# 查看容器退出日志
docker logs app-backend
docker logs app-frontend

# 查看容器详细状态
docker inspect app-backend | grep -A 10 "State"
```

### 问题：前端页面空白

1. 检查前端构建是否成功：`docker logs app-frontend`
2. 进入容器查看是否有静态文件：`docker exec app-frontend ls /usr/share/nginx/html`
3. 检查 Nginx 配置语法：`docker exec app-frontend nginx -t`

### 问题：API 返回 502 Bad Gateway

1. 确认后端容器正在运行：`docker ps`
2. 检查后端健康状态：`docker inspect --format='{{.State.Health.Status}}' app-backend`
3. 查看后端日志：`docker logs app-backend`
4. 确认 Nginx 中的 `proxy_pass` 主机名与 Compose 中的服务名一致（默认为 `backend`）

### 问题：数据库连接失败

1. 检查 PostgreSQL 容器是否运行：`docker ps | grep app-db`
2. 检查数据库健康状态：`docker exec app-db pg_isready -U postgres`
3. 确认 `DATABASE_URL` 中的主机名与 Compose 服务名一致（容器内使用 `db`）
4. 查看 PostgreSQL 日志：`docker logs app-db`
5. 尝试从后端容器手动连接：`docker exec app-backend python -c "import psycopg2; psycopg2.connect('postgresql://postgres:postgres@db:5432/app')"`

### 问题：磁盘空间不足

```bash
# 查看 Docker 磁盘占用
docker system df

# 清理未使用的镜像、容器和网络
docker system prune -f

# 清理所有未使用的镜像（包括悬空镜像）
docker image prune -a -f
```

---

## 14. CI/CD 集成参考

以下为 GitHub Actions 示例，可根据实际 CI 平台调整：

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 构建后端镜像
        run: docker build -f ops/Dockerfile.backend -t app-backend:${{ github.sha }} .

      - name: 构建前端镜像
        run: docker build -f ops/Dockerfile.frontend -t app-frontend:${{ github.sha }} .

      - name: 推送镜像到镜像仓库
        run: |
          docker tag app-backend:${{ github.sha }} registry.example.com/app-backend:${{ github.sha }}
          docker tag app-frontend:${{ github.sha }} registry.example.com/app-frontend:${{ github.sha }}
          docker push registry.example.com/app-backend:${{ github.sha }}
          docker push registry.example.com/app-frontend:${{ github.sha }}

      - name: 部署到服务器
        run: |
          ssh deploy@server "cd /opt/app && git pull && bash ops/scripts/deploy.sh"
```

> 实际使用时需配置 Docker Registry 凭据和 SSH 密钥等 Secrets。
