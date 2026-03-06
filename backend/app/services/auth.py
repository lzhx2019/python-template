"""认证业务逻辑：用户注册与登录。"""

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest


def register_user(session: Session, data: RegisterRequest) -> User:
    """
    注册新用户。
    若用户名或邮箱已存在，返回 409 冲突错误。
    """
    existing = session.exec(select(User).where((User.username == data.username) | (User.email == data.email))).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already registered")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, username: str, password: str) -> str:
    """
    验证用户凭据。
    成功则返回 JWT 访问令牌，失败抛出 401 异常。
    """
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return create_access_token(subject=str(user.id))
