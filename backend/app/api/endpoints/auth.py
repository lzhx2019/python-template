from fastapi import APIRouter

from app.core.deps import CurrentUser, SessionDep
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse
from app.services.auth import authenticate_user, register_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(session: SessionDep, data: RegisterRequest):
    return register_user(session, data)


@router.post("/login", response_model=TokenResponse)
def login(session: SessionDep, data: RegisterRequest):
    token = authenticate_user(session, data.username, data.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser):
    return current_user
