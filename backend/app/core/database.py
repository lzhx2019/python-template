"""数据库模块：创建引擎、初始化表结构、提供会话依赖。

同时支持 SQLite（开发/测试）和 PostgreSQL（生产）。
引擎参数会根据 DATABASE_URL 的类型自动调整。
"""

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


def _build_engine_kwargs() -> dict:
    """根据数据库类型构建引擎参数。"""
    kwargs: dict = {"echo": False}

    if settings.is_sqlite:
        # SQLite 需要允许多线程访问
        kwargs["connect_args"] = {"check_same_thread": False}
    else:
        # PostgreSQL 连接池配置
        kwargs["pool_size"] = settings.DB_POOL_SIZE
        kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
        kwargs["pool_pre_ping"] = True  # 自动检测失效连接

    return kwargs


engine = create_engine(settings.DATABASE_URL, **_build_engine_kwargs())


def create_db_and_tables():
    """根据 SQLModel 元数据自动创建所有表（如已存在则跳过）。"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """生成器依赖：为每个请求提供独立的数据库会话，请求结束后自动关闭。"""
    with Session(engine) as session:
        yield session
