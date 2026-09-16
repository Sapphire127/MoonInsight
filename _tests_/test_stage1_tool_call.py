"""阶段 ① 集成测试：单次工具调用往返（真实 LLM）。

无 LLM_API_KEY 时跳过；有 key 时验证完整链路：
提问算术 → 模型发起 calculator 工具调用 → 代码计算 → 回填 → 最终回答含正确数字。
"""

import os

import pytest

from moon_insight.adapters.deepseek_llm import DeepSeekLLM
from moon_insight.domain.tools import TOOLS
from moon_insight.pipeline.tool_call import run_tool_call_round

pytestmark = pytest.mark.skipif(
    not os.environ.get("LLM_API_KEY"),
    reason="LLM_API_KEY 未配置，跳过真实调用测试",
)


def test_calculator_tool_call_round() -> None:
    provider = DeepSeekLLM()
    result = run_tool_call_round(provider, TOOLS, "请计算 (3+5)*2 的结果")

    assert result["tool_calls"], "模型应发起至少一次 calculator 工具调用"
    assert result["tool_calls"][0]["name"] == "calculator"
    assert result["tool_calls"][0]["result"] == "16"
    assert "16" in result["final_answer"]
