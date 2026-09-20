"""脚本化 Fake LLM：确定性回放，零 API 成本。

LLMProvider 端口的 fake 实现，分两类：

- ScriptedLLM：纯回放器——按注入脚本依次返回响应，零理解逻辑。
  路径穷举（多工具、错误、坏 JSON、hit_limit 等）用它显式脚本完成；
- DemoLLM：E2E 演示回放器（MOON_INSIGHT_LLM=fake 时由组装层注入，
  见 interfaces/main.py）——按各段对话的首个问题在两条封顶路径中选择：
  直接回答 / 两轮 calculator 多步计算。仅覆盖链路渲染验证，不扩展。

真实 LLM 的集成测试见 _tests_/test_stage1_tool_call.py，两者分工互补。
"""

import json
from typing import Any

DIRECT_ANSWER = "这是脚本化直接回答（fake LLM）。"
MULTI_STEP_ANSWER = "结果是 4"


def tool_call_response(call_id: str, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """脚本项构造器：一条含单个工具调用的 LLM 响应。"""
    return {
        "choices": [
            {
                "message": {
                    "content": None,
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": name,
                                "arguments": json.dumps(arguments),
                            },
                        }
                    ],
                }
            }
        ]
    }


def answer_response(content: str) -> dict[str, Any]:
    """脚本项构造器：一条最终回答 LLM 响应。"""
    return {"choices": [{"message": {"content": content}}]}


_MULTI_STEP_SCRIPT = [
    tool_call_response("call_1", "calculator", {"expression": "(3+5)*2"}),
    tool_call_response("call_2", "calculator", {"expression": "16/4"}),
    answer_response(MULTI_STEP_ANSWER),
]
_DIRECT_SCRIPT = [answer_response(DIRECT_ANSWER)]


class ScriptedLLM:
    """纯回放器：按注入脚本依次返回响应，不做任何问题理解。

    脚本耗尽时抛 RuntimeError——测试脚本未覆盖循环全程属于测试缺陷，
    应显式失败而非静默重复。
    """

    def __init__(self, script: list[dict[str, Any]]) -> None:
        self._script = list(script)
        self._position = 0

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self._position >= len(self._script):
            raise RuntimeError("ScriptedLLM: script exhausted before loop finished")
        response = self._script[self._position]
        self._position += 1
        return response


class DemoLLM:
    """E2E 演示回放器：按每段对话的首个问题选择两条封顶路径之一回放。

    对话起点特征：消息列表仅一条 user 消息。同一实例可服务多段对话
    （组装层 lru_cache 单例，页面连续提问依赖此重置）。

    仅覆盖「直接回答 / 多步工具调用」两条链路渲染路径；
    路径穷举请用 ScriptedLLM 显式脚本（pytest 层）。
    """

    def __init__(self) -> None:
        self._impl: ScriptedLLM | None = None

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if len(messages) == 1 and messages[0].get("role") == "user":
            user_text = messages[0].get("content") or ""
            multi_step = "除以" in user_text or "÷" in user_text
            self._impl = ScriptedLLM(_MULTI_STEP_SCRIPT if multi_step else _DIRECT_SCRIPT)
        return self._impl.chat(messages, tools=tools, json_schema=json_schema)
