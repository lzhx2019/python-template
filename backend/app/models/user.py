"""用户数据模型：对应数据库 users 表。"""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """用户表模型。"""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=64)  # 用户名，唯一
    email: str = Field(unique=True, index=True, max_length=255)  # 邮箱，唯一
    hashed_password: str  # bcrypt 哈希后的密码
    is_active: bool = Field(default=True)  # 是否激活
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))  # 创建时间（UTC）
