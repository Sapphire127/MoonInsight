"""fake_llm 模块测试：显式脚本回放器与 E2E 演示回放器。

E2E（web/e2e/）验证 HTTP + 前端渲染链路，本文件验证回放器在循环层的
确定性行为、脚本耗尽保护与组装层 env 开关契约。
"""

import pytest

from moon_insight.application.tool_call import run_agent_loop
from moon_insight.demo_tools import TOOLS, execute_demo_tool
from moon_insight.infrastructure.fake_llm import (
    DIRECT_ANSWER,
    MULTI_STEP_ANSWER,
    DemoLLM,
    ScriptedLLM,
    answer_response,
    tool_call_response,
)


def test_direct_answer_script() -> None:
    """无工具调用路径：脚本首项即回答，与自然语言问题无关。"""
    script = [answer_response(DIRECT_ANSWER)]

    result = run_agent_loop(ScriptedLLM(script), TOOLS, "任意问题", execute_demo_tool)

    assert result["final_answer"] == DIRECT_ANSWER
    assert result["tool_calls"] == []
    assert result["steps"] == 0
    assert result["hit_limit"] is False


def test_multi_step_script() -> None:
    """多步路径：两轮 calculator 调用（真实执行器求值）后作答。"""
    script = [
        tool_call_response("call_1", "calculator", {"expression": "(3+5)*2"}),
        tool_call_response("call_2", "calculator", {"expression": "16/4"}),
        answer_response(MULTI_STEP_ANSWER),
    ]

    result = run_agent_loop(ScriptedLLM(script), TOOLS, "任意问题", execute_demo_tool)

    assert [call["result"] for call in result["tool_calls"]] == ["16", "4"]
    assert result["final_answer"] == MULTI_STEP_ANSWER
    assert result["steps"] == 2
    assert result["hit_limit"] is False


def test_script_exhausted_raises() -> None:
    """脚本未覆盖循环全程时应显式失败，而非静默重复。"""
    script = [tool_call_response("call_1", "calculator", {"expression": "1+1"})]

    with pytest.raises(RuntimeError, match="exhausted"):
        run_agent_loop(ScriptedLLM(script), TOOLS, "先算一次", execute_demo_tool)


def test_demo_llm_serves_multiple_conversations() -> None:
    """E2E 演示回放器：同一实例服务多段对话，按各自首个问题选择路径。"""
    demo = DemoLLM()

    direct = run_agent_loop(demo, TOOLS, "FASTAPI是什么？", execute_demo_tool)
    assert direct["final_answer"] == DIRECT_ANSWER
    assert direct["tool_calls"] == []

    multi = run_agent_loop(
        demo, TOOLS, "先计算 (3+5)*2，再把结果除以 4", execute_demo_tool
    )
    assert [call["result"] for call in multi["tool_calls"]] == ["16", "4"]
    assert multi["final_answer"] == MULTI_STEP_ANSWER


def test_get_provider_fake_switch(monkeypatch: pytest.MonkeyPatch) -> None:
    """组装层契约：MOON_INSIGHT_LLM=fake 时注入演示回放器（E2E 依赖此开关）。"""
    from moon_insight.interfaces.main import get_provider

    monkeypatch.setenv("MOON_INSIGHT_LLM", "fake")
    get_provider.cache_clear()
    try:
        assert isinstance(get_provider(), DemoLLM)
    finally:
        get_provider.cache_clear()
