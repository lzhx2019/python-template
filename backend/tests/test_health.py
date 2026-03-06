"""健康检查接口测试。"""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """验证 /health 接口返回正确的状态响应。"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


def test_health_check_contains_required_fields(client: TestClient):
    """验证响应中包含 status 和 database 字段。"""
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert "database" in data
