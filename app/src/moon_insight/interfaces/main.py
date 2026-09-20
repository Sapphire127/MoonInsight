"""FastAPI 交付层：问答接口。

前端 `web/` 经 dev 代理把 /api/* 转发到本服务（见 architecture.md 布局约定）。
使用端是唯一组装点：在此把适配器与演示工具注入 pipeline。
流式（SSE 等）待拍板，当前为普通 JSON。
"""

import os
from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from moon_insight.demo_tools import TOOLS, execute_demo_tool
from moon_insight.application.tool_call import run_agent_loop
from moon_insight.domain.ports.llm import LLMProvider
from moon_insight.infrastructure.deepseek_llm import DeepSeekLLM
from moon_insight.infrastructure.fake_llm import DemoLLM

app = FastAPI(title="MoonInsight", version="0.1.0")


@lru_cache
def get_provider() -> LLMProvider:
    """依赖注入点：测试用 app.dependency_overrides 替换为 fake。

    MOON_INSIGHT_LLM=fake 时注入 E2E 演示回放器 DemoLLM（确定性、零 API 成本）。
    """
    if os.environ.get("MOON_INSIGHT_LLM") == "fake":
        return DemoLLM()
    return DeepSeekLLM()


class ChatRequest(BaseModel):
    message: str


@app.get("/api/hello")
def hello() -> dict[str, str]:
    return {"message": "Hello from MoonInsight backend"}


@app.post("/api/chat")
def chat(
    req: ChatRequest,
    provider: Annotated[LLMProvider, Depends(get_provider)],
) -> dict[str, Any]:
    """一次非流式问答：用户消息 → Agent 工具调用循环 → 最终回答。"""
    return run_agent_loop(provider, TOOLS, req.message, execute_demo_tool)
