"""数据模型包：在此统一导出所有 SQLModel 模型，确保 metadata 能正确收集表定义。"""

from app.models.user import User

__all__ = ["User"]
