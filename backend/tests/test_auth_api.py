"""认证 API 接口集成测试：注册、登录、获取当前用户。"""

from fastapi.testclient import TestClient

from app.models.user import User

# ==================== 注册接口 ====================


class TestRegister:
    """POST /api/v1/auth/register"""

    def test_register_success(self, client: TestClient):
        """正常注册返回用户信息。"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "newuser", "email": "new@example.com", "password": "secret123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert data["is_active"] is True
        assert "id" in data

    def test_register_response_excludes_password(self, client: TestClient):
        """注册响应中不应包含密码字段。"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "user1", "email": "u1@example.com", "password": "pass"},
        )
        data = response.json()
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_username(self, client: TestClient, test_user: User):
        """注册已存在的用户名应返回 409。"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "testuser", "email": "other@example.com", "password": "pass"},
        )
        assert response.status_code == 409

    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """注册已存在的邮箱应返回 409。"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "otheruser", "email": "test@example.com", "password": "pass"},
        )
        assert response.status_code == 409

    def test_register_invalid_email(self, client: TestClient):
        """无效邮箱格式应返回 422 校验错误。"""
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "user2", "email": "not-an-email", "password": "pass"},
        )
        assert response.status_code == 422

    def test_register_missing_fields(self, client: TestClient):
        """缺少必填字段应返回 422。"""
        response = client.post("/api/v1/auth/register", json={"username": "user3"})
        assert response.status_code == 422

    def test_register_empty_body(self, client: TestClient):
        """空请求体应返回 422。"""
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422


# ==================== 登录接口 ====================


class TestLogin:
    """POST /api/v1/auth/login"""

    def test_login_success(self, client: TestClient, test_user: User):
        """正确凭据应返回 JWT 令牌。"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """错误密码应返回 401。"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "email": "test@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """不存在的用户应返回 401。"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "nobody", "email": "nobody@example.com", "password": "pass"},
        )
        assert response.status_code == 401

    def test_login_returns_valid_jwt(self, client: TestClient, test_user: User):
        """登录返回的令牌应能成功解码且 sub 为用户 ID。"""
        from app.core.security import decode_access_token

        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"},
        )
        token = response.json()["access_token"]
        payload = decode_access_token(token)
        assert payload["sub"] == str(test_user.id)


# ==================== 获取当前用户接口 ====================


class TestMe:
    """GET /api/v1/auth/me"""

    def test_me_authenticated(self, client: TestClient, test_user: User, auth_headers: dict):
        """已认证用户应返回自身信息。"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["is_active"] is True

    def test_me_no_token(self, client: TestClient):
        """无令牌访问应返回 401。"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_me_invalid_token(self, client: TestClient):
        """无效令牌应返回 401。"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401

    def test_me_expired_token(self, client: TestClient, test_user: User):
        """过期令牌应返回 401。"""
        from datetime import timedelta

        from app.core.security import create_access_token

        expired_token = create_access_token(subject=str(test_user.id), expires_delta=timedelta(seconds=-1))
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401

    def test_me_token_nonexistent_user(self, client: TestClient):
        """令牌中的用户 ID 不存在应返回 401。"""
        from app.core.security import create_access_token

        token = create_access_token(subject="99999")
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    def test_me_token_missing_sub(self, client: TestClient):
        """令牌载荷缺少 sub 字段应返回 401。"""
        import jwt as pyjwt

        from app.core.config import settings

        token = pyjwt.encode(
            {"exp": 9999999999},
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    def test_me_response_excludes_password(self, client: TestClient, auth_headers: dict):
        """当前用户响应中不应包含密码。"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        data = response.json()
        assert "password" not in data
        assert "hashed_password" not in data
