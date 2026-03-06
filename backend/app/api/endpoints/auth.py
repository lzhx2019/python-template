"""认证接口：注册、登录、获取当前用户。"""

from fastapi import APIRouter

from app.core.deps import CurrentUser, SessionDep
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse
from app.services.auth import authenticate_user, register_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(session: SessionDep, data: RegisterRequest):
    """注册新用户并返回用户信息。"""
    return register_user(session, data)


@router.post("/login", response_model=TokenResponse)
def login(session: SessionDep, data: RegisterRequest):
    """用户登录，验证成功后返回 JWT 令牌。"""
    token = authenticate_user(session, data.username, data.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser):
    """获取当前已认证用户的信息。"""
    return current_user
