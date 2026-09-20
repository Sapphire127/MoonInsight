"""阶段 ② 测试：步数上限触发（脚本回放持续要求工具调用）。"""

from moon_insight.application.tool_call import run_agent_loop
from moon_insight.demo_tools import execute_demo_tool
from moon_insight.infrastructure.fake_llm import (
    ScriptedLLM,
    answer_response,
    tool_call_response,
)


def test_hits_max_steps() -> None:
    """max_steps=2：两轮工具调用后触发上限，补一次最终回答并标记 hit_limit。

    脚本恰好覆盖全程（2 次工具调用 + 1 次最终回答）；若循环行为变化
    导致脚本未覆盖，回放器会显式抛错，暴露覆盖不足。
    """
    script = [
        tool_call_response("call_1", "calculator", {"expression": "1+1"}),
        tool_call_response("call_2", "calculator", {"expression": "2+2"}),
        answer_response("最终回答"),
    ]

    result = run_agent_loop(
        ScriptedLLM(script), [], "一直算", execute_demo_tool, max_steps=2
    )

    assert result["hit_limit"] is True
    assert result["steps"] == 2
    assert len(result["tool_calls"]) == 2
    assert result["final_answer"] == "最终回答"
