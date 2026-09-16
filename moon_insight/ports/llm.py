"""LLMProvider 端口：LLM 接入的可替换性边界。

已锁决策 1：OpenAI SDK 兼容格式接入，屏蔽供应商差异；
各任务 per-task 可换模型。接口形状为初始草案，随首个实现细化。
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """兼容 OpenAI 格式的 LLM 接入端口。"""

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        json_schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发起一次对话补全。

        结构化输出（已锁决策 2）通过 json_schema 约束返回形状。
        """
        ...
