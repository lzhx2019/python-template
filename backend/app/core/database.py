"""数据库模块：创建引擎、初始化表结构、提供会话依赖。"""

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# 创建数据库引擎（echo=False 关闭 SQL 日志输出）
engine = create_engine(settings.DATABASE_URL, echo=False)


def create_db_and_tables():
    """根据 SQLModel 元数据自动创建所有表（如已存在则跳过）。"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """生成器依赖：为每个请求提供独立的数据库会话，请求结束后自动关闭。"""
    with Session(engine) as session:
        yield session
