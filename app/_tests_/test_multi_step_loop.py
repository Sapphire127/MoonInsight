"""阶段 ② 测试：多轮工具调用循环（显式脚本回放，零 API 成本）。

问题需要两步计算：先 (3+5)*2，再把结果除以 4。
脚本前两轮各返回一次工具调用，第三轮返回最终回答。
"""

from moon_insight.application.tool_call import run_agent_loop
from moon_insight.demo_tools import execute_demo_tool
from moon_insight.infrastructure.fake_llm import (
    MULTI_STEP_ANSWER,
    ScriptedLLM,
    answer_response,
    tool_call_response,
)

SCRIPT = [
    tool_call_response("call_1", "calculator", {"expression": "(3+5)*2"}),
    tool_call_response("call_2", "calculator", {"expression": "16/4"}),
    answer_response(MULTI_STEP_ANSWER),
]


def test_multi_step_loop_runs_two_tool_rounds() -> None:
    result = run_agent_loop(
        ScriptedLLM(SCRIPT), [], "先算 (3+5)*2 再除以 4", execute_demo_tool
    )

    assert len(result["tool_calls"]) == 2
    assert result["tool_calls"][0]["result"] == "16"
    assert result["tool_calls"][1]["result"] == "4"
    assert result["steps"] == 2
    assert result["hit_limit"] is False
    assert "4" in result["final_answer"]
