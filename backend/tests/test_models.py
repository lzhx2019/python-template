"""数据模型单元测试。"""

from datetime import UTC, datetime

from sqlmodel import Session, select

from app.core.security import hash_password, verify_password
from app.models.user import User


class TestUserModel:
    """User 模型测试。"""

    def test_create_user(self, session: Session):
        """应能成功创建用户并持久化到数据库。"""
        user = User(
            username="alice",
            email="alice@example.com",
            hashed_password=hash_password("pass"),
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)

    def test_user_password_is_hashed(self, session: Session):
        """存储的密码应为哈希值而非明文。"""
        user = User(
            username="bob",
            email="bob@example.com",
            hashed_password=hash_password("mypassword"),
        )
        session.add(user)
        session.commit()

        assert user.hashed_password != "mypassword"
        assert verify_password("mypassword", user.hashed_password)

    def test_user_default_is_active(self, session: Session):
        """新建用户默认 is_active 为 True。"""
        user = User(
            username="carol",
            email="carol@example.com",
            hashed_password="hash",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.is_active is True

    def test_user_created_at_is_utc(self, session: Session):
        """created_at 应为 UTC 时间。"""
        user = User(
            username="dave",
            email="dave@example.com",
            hashed_password="hash",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        now = datetime.now(UTC)
        assert abs((now - user.created_at.replace(tzinfo=UTC)).total_seconds()) < 5

    def test_query_user_by_username(self, session: Session):
        """应能通过用户名查询到用户。"""
        user = User(username="eve", email="eve@example.com", hashed_password="hash")
        session.add(user)
        session.commit()

        result = session.exec(select(User).where(User.username == "eve")).first()
        assert result is not None
        assert result.email == "eve@example.com"

    def test_query_user_by_email(self, session: Session):
        """应能通过邮箱查询到用户。"""
        user = User(username="frank", email="frank@example.com", hashed_password="hash")
        session.add(user)
        session.commit()

        result = session.exec(select(User).where(User.email == "frank@example.com")).first()
        assert result is not None
        assert result.username == "frank"

    def test_multiple_users(self, session: Session):
        """应能创建多个用户并全部查询出来。"""
        for i in range(5):
            session.add(User(username=f"user{i}", email=f"user{i}@example.com", hashed_password="hash"))
        session.commit()

        users = session.exec(select(User)).all()
        assert len(users) == 5
