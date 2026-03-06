"""测试公共 fixtures：提供隔离的 SQLite 测试数据库、测试客户端和预置用户。"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.database import get_session
from app.core.security import hash_password
from app.main import app
from app.models.user import User

# 使用 SQLite 内存数据库，每次测试独立
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


def _override_get_session():
    """替换应用的数据库会话为测试数据库会话。"""
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = _override_get_session


@pytest.fixture(autouse=True)
def setup_database():
    """每个测试前创建所有表，测试后销毁，保证隔离。"""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def session():
    """提供一个测试数据库会话。"""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client():
    """提供已绑定测试数据库的 TestClient。"""
    return TestClient(app)


@pytest.fixture
def test_user(session: Session) -> User:
    """预置一个测试用户（密码为 'password123'）。"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User) -> dict:
    """预置用户登录后的认证请求头。"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
