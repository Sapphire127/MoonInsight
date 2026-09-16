"""冒烟测试：验证交付层的最小调用链。"""

from fastapi.testclient import TestClient

from moon_insight.api.main import app

client = TestClient(app)


def test_hello_returns_200_and_message() -> None:
    resp = client.get("/api/hello")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello from MoonInsight backend"}
