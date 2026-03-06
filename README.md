# 全栈项目脚手架

基于 React 前端 + FastAPI 后端的全栈 Web 应用脚手架。

## 技术栈

### 前端（`frontend/`）

| 技术         | 用途             |
| ------------ | ---------------- |
| React 18     | UI 框架          |
| Vite         | 构建工具 & 开发服务器 |
| TypeScript   | 类型安全          |
| Zustand      | 状态管理          |
| React Router | 客户端路由         |
| Axios        | HTTP 请求库       |
| Less         | CSS 预处理器       |
| ESLint       | 代码检查          |

### 后端（`backend/`）

| 技术        | 用途             |
| ----------- | ---------------- |
| Python 3.12 | 运行时            |
| FastAPI     | Web 框架          |
| Pydantic    | 数据校验          |
| SQLModel    | ORM（基于 SQLAlchemy）|
| PyJWT       | JWT 身份认证       |
| uv          | 包管理器          |

## 项目结构

```
.
├── frontend/                  # React 前端
│   ├── src/
│   │   ├── components/        # 可复用组件
│   │   ├── pages/             # 页面级组件
│   │   ├── stores/            # Zustand 状态仓库
│   │   ├── styles/            # 全局样式 & Less 变量
│   │   ├── types/             # TypeScript 类型定义
│   │   ├── utils/             # 工具函数（axios 封装等）
│   │   ├── App.tsx            # 根组件（路由配置）
│   │   └── main.tsx           # 入口文件
│   ├── eslint.config.js
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── package.json
├── backend/                   # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   └── endpoints/     # 路由处理函数
│   │   ├── core/              # 配置、数据库、安全、依赖注入
│   │   ├── models/            # SQLModel 数据模型
│   │   ├── schemas/           # Pydantic 请求/响应模式
│   │   └── services/          # 业务逻辑层
│   ├── tests/                 # 测试
│   ├── pyproject.toml         # Python 项目配置 & 依赖声明
│   └── .python-version        # 锁定 Python 版本（3.12.12）
└── README.md
```

## 快速开始

### 环境要求

- [Node.js](https://nodejs.org/) >= 18
- [uv](https://docs.astral.sh/uv/)（Python 包管理器）

### 启动后端

```bash
cd backend

# 安装依赖（uv 会自动创建虚拟环境）
uv sync

# 复制环境变量配置
cp .env.example .env

# 启动开发服务器
uv run uvicorn app.main:app --reload
```

API 地址：**http://localhost:8000**
交互式 API 文档：**http://localhost:8000/docs**

### 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

应用地址：**http://localhost:5173**
前端已配置 Vite 代理，`/api` 请求会自动转发至后端。

### 运行测试

```bash
# 后端测试
cd backend
uv run pytest

# 前端代码检查
cd frontend
npm run lint
```

## API 接口

| 方法 | 路径                    | 说明           |
| ---- | ----------------------- | -------------- |
| GET  | `/health`               | 健康检查        |
| POST | `/api/v1/auth/register` | 注册新用户      |
| POST | `/api/v1/auth/login`    | 登录并获取 JWT  |
| GET  | `/api/v1/auth/me`       | 获取当前用户信息 |

## 许可证

详见 [LICENSE](./LICENSE)。
