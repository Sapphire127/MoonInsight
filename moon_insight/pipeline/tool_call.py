"""阶段 ①：单次工具调用往返。

用户消息 → LLM（携带工具定义）→ 模型返回 tool_calls → 代码执行工具 →
结果回填 → LLM 给出最终回答。带步数上限的完整循环在阶段 ② 引入。
"""

import json
from typing import Any

from moon_insight.domain.tools import execute_tool
from moon_insight.ports.llm import LLMProvider


def run_tool_call_round(
    provider: LLMProvider,
    tools: list[dict[str, Any]],
    user_message: str,
) -> dict[str, Any]:
    """执行一次「提问 → 工具调用 → 回填 → 回答」往返。

    返回 {"final_answer": str, "tool_calls": [...]}。
    """
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": user_message}
    ]

    first = provider.chat(messages, tools=tools)
    message = first["choices"][0]["message"]

    tool_calls: list[dict[str, Any]] = []
    if message.get("tool_calls"):
        messages.append(message)  # assistant 消息（含 tool_calls）
        for call in message["tool_calls"]:
            fn = call["function"]
            arguments = json.loads(fn["arguments"] or "{}")
            result = execute_tool(fn["name"], arguments)
            tool_calls.append(
                {"name": fn["name"], "arguments": arguments, "result": result}
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": result,
                }
            )
        final = provider.chat(messages, tools=tools)
        message = final["choices"][0]["message"]

    return {
        "final_answer": message.get("content") or "",
        "tool_calls": tool_calls,
    }
