"""全局配置模块：通过环境变量或 .env 文件加载应用配置。"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置项，支持从环境变量和 .env 文件读取。"""

    # --- 基本信息 ---
    PROJECT_NAME: str = "FastAPI Backend"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # --- 数据库 ---
    # 支持 SQLite 和 PostgreSQL，通过 DATABASE_URL 切换：
    #   SQLite:      sqlite:///./app.db
    #   PostgreSQL:  postgresql://user:password@localhost:5432/dbname
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/app"

    # PostgreSQL 连接池配置（仅对 PostgreSQL 生效）
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # --- JWT 认证 ---
    SECRET_KEY: str = "change-me-in-production"  # 生产环境务必修改
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 令牌有效期：24 小时

    # --- 跨域 ---
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")


# 全局单例配置对象
settings = Settings()
