"""API 路由汇总：将各模块的路由统一注册到主路由器。"""

from fastapi import APIRouter

from app.api.endpoints import auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
