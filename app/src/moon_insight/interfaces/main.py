"""FastAPI 交付层：问答接口。

前端 `web/` 经 dev 代理把 /api/* 转发到本服务（见 architecture.md 布局约定）。
使用端是唯一组装点：在此把适配器与演示工具注入 pipeline。
流式（SSE 等）待拍板，当前为普通 JSON。
"""

from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from moon_insight.demo_tools import TOOLS, execute_demo_tool
from moon_insight.application.tool_call import run_tool_call_round
from moon_insight.domain.ports.llm import LLMProvider
from moon_insight.infrastructure.deepseek_llm import DeepSeekLLM

app = FastAPI(title="MoonInsight", version="0.1.0")


@lru_cache
def get_provider() -> LLMProvider:
    """依赖注入点：测试用 app.dependency_overrides 替换为 fake。"""
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
    """一次非流式问答：用户消息 → Agent 工具调用往返 → 最终回答。"""
    return run_tool_call_round(provider, TOOLS, req.message, execute_demo_tool)
