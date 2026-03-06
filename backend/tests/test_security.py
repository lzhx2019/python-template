"""安全工具单元测试：密码哈希与 JWT 令牌。"""

from datetime import timedelta

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    """密码哈希相关测试。"""

    def test_hash_password_returns_bcrypt_string(self):
        """哈希结果应为 bcrypt 格式（以 $2b$ 开头）。"""
        hashed = hash_password("mysecret")
        assert hashed.startswith("$2b$")

    def test_hash_password_different_each_time(self):
        """相同密码每次哈希结果不同（盐值随机）。"""
        h1 = hash_password("mysecret")
        h2 = hash_password("mysecret")
        assert h1 != h2

    def test_verify_password_correct(self):
        """正确密码应验证通过。"""
        hashed = hash_password("mysecret")
        assert verify_password("mysecret", hashed) is True

    def test_verify_password_wrong(self):
        """错误密码应验证失败。"""
        hashed = hash_password("mysecret")
        assert verify_password("wrongpassword", hashed) is False

    def test_verify_password_empty(self):
        """空密码应验证失败。"""
        hashed = hash_password("mysecret")
        assert verify_password("", hashed) is False


class TestJWT:
    """JWT 令牌相关测试。"""

    def test_create_and_decode_token(self):
        """生成的令牌应能正确解码，且 sub 字段一致。"""
        token = create_access_token(subject="42")
        payload = decode_access_token(token)
        assert payload["sub"] == "42"
        assert "exp" in payload

    def test_token_with_custom_expiry(self):
        """自定义过期时间应被正确设置。"""
        token = create_access_token(subject="1", expires_delta=timedelta(minutes=5))
        payload = decode_access_token(token)
        assert payload["sub"] == "1"

    def test_decode_invalid_token_raises(self):
        """解码无效令牌应抛出异常。"""
        with pytest.raises(jwt.PyJWTError):
            decode_access_token("invalid.token.here")

    def test_decode_token_with_wrong_secret(self):
        """使用错误密钥签发的令牌应解码失败。"""
        token = jwt.encode(
            {"sub": "1", "exp": 9999999999},
            "wrong-secret",
            algorithm=settings.JWT_ALGORITHM,
        )
        with pytest.raises(jwt.InvalidSignatureError):
            decode_access_token(token)

    def test_decode_expired_token_raises(self):
        """已过期的令牌应解码失败。"""
        token = create_access_token(subject="1", expires_delta=timedelta(seconds=-1))
        with pytest.raises(jwt.ExpiredSignatureError):
            decode_access_token(token)
