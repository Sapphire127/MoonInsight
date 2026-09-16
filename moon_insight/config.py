"""应用配置：环境变量读取的最小实现。

密钥边界从第一天正确：敏感值只经环境变量/`.env` 进入，永不写进代码。
hello world 阶段只有端口一项真实配置，其余随步骤补。
"""

import os

BACKEND_PORT: int = int(os.environ.get("BACKEND_PORT", "8000"))

# LLM 接入（已锁决策 ①：OpenAI 兼容格式；模型是配置项非选型）
LLM_API_KEY: str = os.environ.get("LLM_API_KEY", "")
LLM_BASE_URL: str = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL: str = os.environ.get("LLM_MODEL", "deepseek-chat")
