"""认证相关的请求/响应数据模式。"""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """注册请求体。"""

    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """登录请求体。"""

    username: str
    password: str


class TokenResponse(BaseModel):
    """登录成功后返回的令牌。"""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """用户信息响应体（不包含密码等敏感字段）。"""

    id: int
    username: str
    email: str
    is_active: bool
