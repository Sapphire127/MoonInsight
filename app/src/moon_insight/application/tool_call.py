"""阶段 ②：带步数上限的 Agent 循环。

Reason（LLM 决策）→ Act（执行工具）→ Observe（回填结果）→ Repeat，
直到模型不再发起工具调用或触达步数上限（防死循环）。

工具定义与执行器均由使用端注入——application 不 import 任何具体工具。
"""

import json
from collections.abc import Callable
from typing import Any

from moon_insight.domain.ports.llm import LLMProvider

ToolExecutor = Callable[[str, dict[str, Any]], str]

MAX_STEPS = 4


def run_agent_loop(
    provider: LLMProvider,
    tools: list[dict[str, Any]],
    user_message: str,
    executor: ToolExecutor,
    max_steps: int = MAX_STEPS,
) -> dict[str, Any]:
    """运行「决策 → 执行 → 观察」循环，直到模型给出最终回答。

    返回 {"final_answer": str, "tool_calls": [...], "steps": int,
    "hit_limit": bool}——steps 与 hit_limit 供运行记录与前端展示。
    """
    messages: list[dict[str, Any]] = [{"role": "user", "content": user_message}]
    tool_calls: list[dict[str, Any]] = []
    steps = 0

    while steps < max_steps:
        resp = provider.chat(messages, tools=tools)
        message = resp["choices"][0]["message"]
        if not message.get("tool_calls"):
            return {
                "final_answer": message.get("content") or "",
                "tool_calls": tool_calls,
                "steps": steps,
                "hit_limit": False,
            }
        messages.append(message)  # assistant 消息（含 tool_calls）
        for call in message["tool_calls"]:
            fn = call["function"]
            arguments = json.loads(fn["arguments"] or "{}")
            result = executor(fn["name"], arguments)
            tool_calls.append(
                {"name": fn["name"], "arguments": arguments, "result": result}
            )
            messages.append(
                {"role": "tool", "tool_call_id": call["id"], "content": result}
            )
        steps += 1

    # 触达上限：再请求一次最终回答，并标记 hit_limit
    final = provider.chat(messages, tools=tools)
    return {
        "final_answer": final["choices"][0]["message"].get("content") or "",
        "tool_calls": tool_calls,
        "steps": steps,
        "hit_limit": True,
    }
