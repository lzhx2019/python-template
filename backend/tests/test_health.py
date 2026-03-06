"""健康检查接口测试。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """验证 /health 接口返回正确的状态响应。"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
