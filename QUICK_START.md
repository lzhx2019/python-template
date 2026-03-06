# 新人快速开发指南

本文档面向刚接手项目的开发者，帮助你在最短时间内搭建本地开发环境、理解项目架构，并完成第一个功能开发。

---

## 目录

1. [环境准备](#1-环境准备)
2. [拉取代码并启动项目](#2-拉取代码并启动项目)
3. [项目架构总览](#3-项目架构总览)
4. [后端开发指南](#4-后端开发指南)
5. [前端开发指南](#5-前端开发指南)
6. [前后端联调](#6-前后端联调)
7. [使用 Docker 开发](#7-使用-docker-开发)
8. [代码规范与检查](#8-代码规范与检查)
9. [测试](#9-测试)
10. [常见问题](#10-常见问题)
11. [延伸阅读](#11-延伸阅读)

---

## 1. 环境准备

开始之前，请确保你的机器上已安装以下工具：

| 工具 | 最低版本 | 安装方式 |
| ---- | -------- | -------- |
| **Node.js** | >= 18 | [官网下载](https://nodejs.org/) 或使用 nvm |
| **npm** | >= 9 | 随 Node.js 自带 |
| **uv** | >= 0.4 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Git** | >= 2.30 | 系统包管理器安装 |
| **Docker**（可选） | >= 24.0 | [官网下载](https://www.docker.com/) |
| **Docker Compose**（可选） | >= 2.20 | Docker Desktop 自带 |

> **提示**：uv 是新一代 Python 包管理器，会自动下载并管理 Python 版本，你**无需**手动安装 Python。

> Docker 为可选项。如果你更习惯容器化开发，可以跳过本地安装 Node.js 和 uv，直接参考[第 7 节：使用 Docker 开发](#7-使用-docker-开发)。

验证安装：

```bash
node -v        # 应输出 v18.x 或更高
npm -v         # 应输出 9.x 或更高
uv --version   # 应输出 uv 0.4.x 或更高
git --version
```

---

## 2. 拉取代码并启动项目

### 2.1 克隆仓库

```bash
git clone <仓库地址>
cd <项目目录>
```

### 2.2 启动后端

```bash
cd backend

# 安装依赖（首次运行会自动下载 Python 3.12.12 并创建虚拟环境）
uv sync

# 复制环境变量配置文件
cp .env.example .env

# 启动开发服务器（支持热重载）
uv run uvicorn app.main:app --reload
```

启动后可访问：
- API 根地址：http://localhost:8000
- 交互式 API 文档（Swagger UI）：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 2.3 启动前端

打开**新的终端窗口**：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

启动后访问 http://localhost:5173 即可看到页面。

> 前端 Vite 开发服务器已配置代理，所有 `/api` 开头的请求会自动转发到后端 `localhost:8000`，无需额外配置跨域。

---

## 3. 项目架构总览

```
.
├── frontend/                      # 前端（React + Vite + TypeScript）
│   ├── src/
│   │   ├── components/            # 可复用组件
│   │   │   └── Layout/            # 全局布局组件
│   │   ├── pages/                 # 页面组件（一个页面一个文件夹）
│   │   │   ├── Home/              # 首页
│   │   │   └── Login/             # 登录页
│   │   ├── stores/                # Zustand 状态仓库
│   │   │   └── useAuthStore.ts    # 认证状态（令牌、用户信息）
│   │   ├── styles/                # 全局样式
│   │   │   ├── global.less        # 全局 CSS 重置
│   │   │   └── variables.less     # Less 变量（颜色、间距等）
│   │   ├── types/                 # TypeScript 类型定义
│   │   ├── utils/                 # 工具函数
│   │   │   └── request.ts         # Axios 请求封装
│   │   ├── App.tsx                # 根组件（路由配置）
│   │   └── main.tsx               # 入口文件
│   ├── vite.config.ts             # Vite 配置（路径别名、代理、Less）
│   ├── tsconfig.json              # TypeScript 配置
│   └── eslint.config.js           # ESLint 配置
│
├── backend/                       # 后端（FastAPI + SQLModel）
│   ├── app/
│   │   ├── api/                   # API 路由层
│   │   │   ├── router.py          # 路由汇总注册
│   │   │   └── endpoints/         # 各模块路由处理函数
│   │   │       └── auth.py        # 认证接口（注册/登录/获取用户）
│   │   ├── core/                  # 核心模块
│   │   │   ├── config.py          # 全局配置（读取 .env）
│   │   │   ├── database.py        # 数据库引擎 & 会话管理
│   │   │   ├── security.py        # 密码哈希 & JWT 工具
│   │   │   └── deps.py            # 公共依赖注入（当前用户等）
│   │   ├── models/                # 数据库模型（SQLModel ORM）
│   │   │   └── user.py            # 用户表模型
│   │   ├── schemas/               # 请求/响应数据模式（Pydantic）
│   │   │   └── auth.py            # 认证相关 Schema
│   │   ├── services/              # 业务逻辑层
│   │   │   └── auth.py            # 认证业务（注册/验证）
│   │   └── main.py                # 应用入口（创建 FastAPI 实例）
│   ├── tests/                     # 测试文件
│   ├── pyproject.toml             # 项目元数据 & 依赖声明
│   ├── .python-version            # Python 版本锁定（3.12.12）
│   └── .env.example               # 环境变量模板
│
├── ops/                           # 部署与运维
│   ├── Dockerfile.backend         # 后端镜像构建
│   ├── Dockerfile.frontend        # 前端镜像构建（Nginx 托管）
│   ├── docker-compose.yml         # 生产环境编排
│   ├── docker-compose.dev.yml     # 开发环境编排（热重载）
│   ├── nginx/
│   │   └── nginx.conf             # Nginx 配置（SPA 回退 + API 反代）
│   ├── scripts/                   # 运维脚本
│   │   ├── deploy.sh              # 一键部署
│   │   ├── stop.sh                # 停止服务
│   │   ├── logs.sh                # 查看日志
│   │   ├── backup.sh              # 数据备份
│   │   └── health-check.sh        # 健康检查
│   └── DEPLOY.md                  # 部署与运维文档
│
├── README.md                      # 项目说明
├── QUICK_START.md                 # 本文档（新人开发指南）
└── LICENSE
```

### 请求流转链路

```
浏览器 → Vite 代理（/api）→ FastAPI → Router → Endpoint → Service → Model/DB
                                                                  ↓
浏览器 ← JSON 响应 ← FastAPI ← Pydantic Schema 序列化 ←──────────┘
```

---

## 4. 后端开发指南

### 4.1 添加新接口的完整流程

以「添加文章 CRUD」为例：

**第一步：创建数据模型** — `backend/app/models/article.py`

```python
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class Article(SQLModel, table=True):
    __tablename__ = "articles"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

别忘了在 `backend/app/models/__init__.py` 中导入新模型：

```python
from app.models.user import User
from app.models.article import Article

__all__ = ["User", "Article"]
```

**第二步：创建请求/响应 Schema** — `backend/app/schemas/article.py`

```python
from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
```

**第三步：编写业务逻辑** — `backend/app/services/article.py`

```python
from sqlmodel import Session, select
from app.models.article import Article
from app.schemas.article import ArticleCreate

def create_article(session: Session, data: ArticleCreate, author_id: int) -> Article:
    article = Article(**data.model_dump(), author_id=author_id)
    session.add(article)
    session.commit()
    session.refresh(article)
    return article

def list_articles(session: Session) -> list[Article]:
    return session.exec(select(Article)).all()
```

**第四步：创建路由** — `backend/app/api/endpoints/article.py`

```python
from fastapi import APIRouter
from app.core.deps import CurrentUser, SessionDep
from app.schemas.article import ArticleCreate, ArticleResponse
from app.services.article import create_article, list_articles

router = APIRouter()

@router.post("/", response_model=ArticleResponse)
def create(session: SessionDep, data: ArticleCreate, user: CurrentUser):
    return create_article(session, data, user.id)

@router.get("/", response_model=list[ArticleResponse])
def list_all(session: SessionDep):
    return list_articles(session)
```

**第五步：注册路由** — 在 `backend/app/api/router.py` 中添加：

```python
from app.api.endpoints import auth, article

api_router.include_router(article.router, prefix="/articles", tags=["articles"])
```

重启服务后访问 http://localhost:8000/docs 即可看到新接口。

### 4.2 环境变量配置

所有配置项集中在 `backend/app/core/config.py` 中，通过 `.env` 文件覆盖默认值：

| 变量名 | 说明 | 默认值 |
| ------ | ---- | ------ |
| `DATABASE_URL` | 数据库连接字符串 | `sqlite:///./app.db` |
| `SECRET_KEY` | JWT 签名密钥 | `change-me-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 令牌有效期（分钟） | `1440`（24 小时） |
| `CORS_ORIGINS` | 允许跨域的前端地址 | `["http://localhost:5173"]` |

### 4.3 常用 uv 命令

```bash
uv sync                  # 安装/同步所有依赖
uv sync --group dev      # 安装开发依赖（pytest、ruff 等）
uv add <包名>            # 添加新依赖
uv add --group dev <包名> # 添加开发依赖
uv run <命令>            # 在虚拟环境中执行命令
uv run python             # 进入 Python REPL
```

---

## 5. 前端开发指南

### 5.1 添加新页面的完整流程

以「添加文章列表页」为例：

**第一步：创建页面组件** — `frontend/src/pages/Articles/index.tsx`

```tsx
import styles from './index.module.less'

export default function Articles() {
  return (
    <div className={styles.container}>
      <h1>文章列表</h1>
    </div>
  )
}
```

**第二步：创建页面样式** — `frontend/src/pages/Articles/index.module.less`

```less
@import '@/styles/variables.less';

.container {
  max-width: 960px;
  margin: 0 auto;
  padding: @spacing-lg;
}
```

**第三步：注册路由** — 在 `frontend/src/App.tsx` 中添加：

```tsx
import Articles from '@/pages/Articles'

// 在 <Route element={<Layout />}> 内添加：
<Route path="/articles" element={<Articles />} />
```

### 5.2 状态管理（Zustand）

项目使用 Zustand 进行状态管理，Store 文件位于 `frontend/src/stores/` 目录。

创建新 Store 的模板：

```typescript
import { create } from 'zustand'

interface ExampleState {
  count: number
  increment: () => void
}

export const useExampleStore = create<ExampleState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))
```

在组件中使用：

```tsx
import { useExampleStore } from '@/stores/useExampleStore'

export default function MyComponent() {
  const { count, increment } = useExampleStore()
  return <button onClick={increment}>{count}</button>
}
```

### 5.3 调用后端接口

项目已封装了 Axios 实例（`frontend/src/utils/request.ts`），会自动处理令牌注入和 401 跳转。

```typescript
import request from '@/utils/request'

// GET 请求
const articles = await request.get<unknown, Article[]>('/articles')

// POST 请求
const newArticle = await request.post<unknown, Article>('/articles', {
  title: '标题',
  content: '内容',
})
```

### 5.4 路径别名

`@` 已配置为 `src/` 目录的别名，推荐始终使用别名导入，保持路径清晰：

```typescript
// 推荐
import { useAuthStore } from '@/stores/useAuthStore'

// 不推荐
import { useAuthStore } from '../../stores/useAuthStore'
```

### 5.5 样式开发

- 使用 **Less CSS Modules**（`*.module.less`），样式自动按组件隔离，无需担心类名冲突
- 公共变量定义在 `frontend/src/styles/variables.less`，在模块样式中通过 `@import` 引用
- 全局样式写在 `frontend/src/styles/global.less`

### 5.6 常用 npm 命令

```bash
npm run dev      # 启动开发服务器（http://localhost:5173）
npm run build    # 生产构建（输出到 dist/）
npm run lint     # ESLint 代码检查
npm run preview  # 预览生产构建结果
```

---

## 6. 前后端联调

1. 确保后端运行在 `localhost:8000`，前端运行在 `localhost:5173`
2. 前端 `vite.config.ts` 中已配置代理规则：所有 `/api` 开头的请求自动转发到后端
3. 打开浏览器开发者工具的 **Network** 面板，可以查看实际请求和响应
4. 后端 Swagger 文档（http://localhost:8000/docs）可以独立测试接口

### 调试技巧

- **后端日志**：uvicorn 默认在终端输出请求日志，出错时查看终端即可
- **前端调试**：使用 React Developer Tools 浏览器插件检查组件状态
- **接口调试**：推荐使用 Swagger UI 或 Postman / Bruno 等工具单独测试后端接口

---

## 7. 使用 Docker 开发

除了本地直接运行前后端外，项目还提供了 Docker Compose 开发环境，适合不想在本机安装 Node.js / Python 的场景。

### 7.1 启动开发环境

```bash
# 准备环境变量
cp ops/.env.example ops/.env

# 一键启动（后端热重载 + 前端 HMR）
docker compose -f ops/docker-compose.dev.yml up --build
```

启动后：
- 前端：http://localhost:5173
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 7.2 开发模式特性

- **后端**：源码目录 `backend/app/` 挂载到容器内，修改 Python 代码后 uvicorn 自动重载
- **前端**：整个 `frontend/` 目录挂载到容器内，修改 TSX/Less 后 Vite HMR 即时生效
- 两个服务共享同一个 Docker 网络，无需额外配置

### 7.3 停止开发环境

```bash
docker compose -f ops/docker-compose.dev.yml down
```

### 7.4 生产构建预览

如果想在本地预览生产环境的完整效果（Nginx 托管 + API 反代）：

```bash
docker compose -f ops/docker-compose.yml up --build
```

访问 http://localhost 即可看到与生产一致的效果。

> 关于正式部署、运维操作、备份恢复等内容，请参阅 [ops/DEPLOY.md](./ops/DEPLOY.md)。

---

## 8. 代码规范与检查

### 后端

- 使用 [Ruff](https://docs.astral.sh/ruff/) 进行代码格式化和 Lint 检查
- 规则配置在 `backend/pyproject.toml` 的 `[tool.ruff]` 部分

```bash
cd backend
uv run ruff check .       # 检查代码
uv run ruff check . --fix # 自动修复
uv run ruff format .      # 格式化代码
```

### 前端

- 使用 ESLint 进行代码检查，规则配置在 `frontend/eslint.config.js`
- TypeScript 严格模式已开启

```bash
cd frontend
npm run lint              # 检查代码
```

### 提交前检查清单

- [ ] 后端：`uv run ruff check .` 无报错
- [ ] 后端：`uv run pytest` 测试通过
- [ ] 前端：`npm run lint` 无报错
- [ ] 前端：`npm run build` 构建成功

---

## 9. 测试

### 后端测试

测试文件位于 `backend/tests/` 目录，使用 pytest 框架：

```bash
cd backend
uv sync --group dev     # 首次需安装开发依赖
uv run pytest           # 运行所有测试
uv run pytest -v        # 详细输出
uv run pytest -k "test_health"  # 运行指定测试
```

编写新测试的示例：

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123",
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

---

## 10. 常见问题

### Q: uv sync 时报 Python 版本找不到？

uv 会自动下载 `.python-version` 中指定的 Python 版本。如果网络受限，可手动安装 Python 3.12 后设置：

```bash
uv python install 3.12.12
```

### Q: 前端启动后页面空白？

1. 检查浏览器控制台是否有报错
2. 确认 `npm install` 已成功执行
3. 尝试清除缓存后重启：`rm -rf node_modules && npm install && npm run dev`

### Q: 后端接口返回 CORS 错误？

确认 `backend/.env` 中的 `CORS_ORIGINS` 包含前端地址：

```
CORS_ORIGINS=["http://localhost:5173"]
```

### Q: 如何切换数据库？

修改 `backend/.env` 中的 `DATABASE_URL`，例如切换到 PostgreSQL：

```
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

同时需要安装对应驱动：`uv add psycopg2-binary`

### Q: 如何添加新的 npm / Python 依赖？

```bash
# 前端
cd frontend && npm install <包名>

# 后端
cd backend && uv add <包名>
```

### Q: Docker 开发环境启动失败？

1. 确认 Docker 和 Docker Compose 已安装并正在运行
2. 检查 `ops/.env` 文件是否已从模板复制：`cp ops/.env.example ops/.env`
3. 查看详细日志：`docker compose -f ops/docker-compose.dev.yml logs`
4. 端口冲突时可在 `ops/.env` 中修改 `BACKEND_PORT` 和 `FRONTEND_PORT`

### Q: Docker 容器内修改代码不生效？

- 开发环境（`docker-compose.dev.yml`）会挂载源码目录，修改应实时生效
- 如果不生效，尝试重启容器：`docker compose -f ops/docker-compose.dev.yml restart`
- 生产环境（`docker-compose.yml`）不挂载源码，修改后需重新构建：`bash ops/scripts/deploy.sh`

---

## 11. 延伸阅读

### 项目文档

| 文档 | 说明 |
| ---- | ---- |
| [README.md](./README.md) | 项目概览、技术栈、API 接口速查 |
| [QUICK_START.md](./QUICK_START.md) | 新人快速开发指南（本文档） |
| [ops/DEPLOY.md](./ops/DEPLOY.md) | 部署与运维文档（Docker 构建、上线流程、备份恢复、故障排查） |

### 前端技术栈

| 资源 | 链接 |
| ---- | ---- |
| React 官方文档 | https://react.dev |
| Vite 官方文档 | https://vite.dev |
| TypeScript 手册 | https://www.typescriptlang.org/docs |
| Zustand 文档 | https://zustand.docs.pmnd.rs |
| React Router 文档 | https://reactrouter.com |
| Less 文档 | https://lesscss.org |

### 后端技术栈

| 资源 | 链接 |
| ---- | ---- |
| FastAPI 官方文档 | https://fastapi.tiangolo.com |
| SQLModel 文档 | https://sqlmodel.tiangolo.com |
| Pydantic 文档 | https://docs.pydantic.dev |
| PyJWT 文档 | https://pyjwt.readthedocs.io |
| uv 文档 | https://docs.astral.sh/uv |

### 部署相关

| 资源 | 链接 |
| ---- | ---- |
| Docker 文档 | https://docs.docker.com |
| Docker Compose 文档 | https://docs.docker.com/compose |
| Nginx 文档 | https://nginx.org/en/docs |

---

> 如果在开发过程中遇到本文档未覆盖的问题，请及时反馈，帮助我们持续完善这份指南。
