"""真实 LLM 集成测试：单步工具调用循环。

无 LLM_API_KEY 时跳过；有 key 时验证完整链路：
提问算术 → 模型发起 calculator 工具调用 → 代码计算 → 回填 → 最终回答含正确数字。
"""

import os

import pytest

from moon_insight.application.tool_call import run_agent_loop
from moon_insight.demo_tools import TOOLS, execute_demo_tool
from moon_insight.infrastructure.deepseek_llm import DeepSeekLLM

pytestmark = pytest.mark.skipif(
    not os.environ.get("LLM_API_KEY"),
    reason="LLM_API_KEY 未配置，跳过真实调用测试",
)


def test_calculator_tool_call_round() -> None:
    provider = DeepSeekLLM()
    result = run_agent_loop(provider, TOOLS, "请计算 (3+5)*2 的结果", execute_demo_tool)

    assert result["tool_calls"], "模型应发起至少一次 calculator 工具调用"
    assert result["tool_calls"][0]["name"] == "calculator"
    assert result["tool_calls"][0]["result"] == "16"
    assert "16" in result["final_answer"]
    assert result["steps"] >= 1
    assert result["hit_limit"] is False
