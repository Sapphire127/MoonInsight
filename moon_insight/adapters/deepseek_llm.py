"""DeepSeek 适配器：LLMProvider 端口实现。

OpenAI SDK 兼容格式（已锁决策 ①）：换供应商只改 base_url 与模型名——
模型是配置项非选型（spec 盘问第一轮 Q5）。
"""

from typing import Any

from openai import OpenAI

from moon_insight.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from moon_insight.ports.llm import LLMProvider


class DeepSeekLLM(LLMProvider):
    """DeepSeek 的 OpenAI 兼容实现。"""

    def __init__(
        self,
        api_key: str = LLM_API_KEY,
        base_url: str = LLM_BASE_URL,
        model: str = LLM_MODEL,
    ) -> None:
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发起一次对话补全，返回 OpenAI 形状的响应 dict。"""
        kwargs: dict[str, Any] = {}
        if tools:
            kwargs["tools"] = tools
        if json_schema:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": json_schema,
            }
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        return resp.model_dump()
