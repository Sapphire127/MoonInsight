"""应用配置：环境变量读取的最小实现。

密钥边界从第一天正确：敏感值只经环境变量/`.env` 进入，永不写进代码。
hello world 阶段只有端口一项真实配置，其余随步骤补。
"""

import os

BACKEND_PORT: int = int(os.environ.get("BACKEND_PORT", "8000"))
