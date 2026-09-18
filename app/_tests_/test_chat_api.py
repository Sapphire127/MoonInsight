"""POST /api/chat 测试：注入 fake provider，不产生真实 LLM 调用。

依赖注入的第一次兑现：测试用预设响应的 fake 替换 DeepSeek，
断言工具调用往返与最终回答，零 API 成本。
"""

from typing import Any

from fastapi.testclient import TestClient

from moon_insight.interfaces.main import app, get_provider


class FakeLLM:
    """预设响应：首轮返回 calculator 工具调用，次轮返回最终回答。"""

    def __init__(self) -> None:
        self.calls = 0

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.calls += 1
        if self.calls == 1:
            return {
                "choices": [
                    {
                        "message": {
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": "call_1",
                                    "type": "function",
                                    "function": {
                                        "name": "calculator",
                                        "arguments": '{"expression": "(3+5)*2"}',
                                    },
                                }
                            ],
                        }
                    }
                ]
            }
        return {"choices": [{"message": {"content": "结果是 16"}}]}


fake = FakeLLM()
app.dependency_overrides[get_provider] = lambda: fake

client = TestClient(app)


def test_chat_endpoint_runs_tool_call_round() -> None:
    resp = client.post("/api/chat", json={"message": "请计算 (3+5)*2"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["tool_calls"][0]["name"] == "calculator"
    assert data["tool_calls"][0]["result"] == "16"
    assert "16" in data["final_answer"]
    assert fake.calls == 2
