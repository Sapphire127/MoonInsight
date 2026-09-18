"""金融助手 Agent —— 顶层包。

后端四层架构：domain（纯逻辑 + 端口抽象）/ application（用例编排）/
infrastructure（端口实现）/ interfaces（交付与组装）/ schemas。
依赖方向：interfaces → application → domain；infrastructure 实现
domain 的端口抽象，由 interfaces 注入。eval / observability / mcp / cli
随步骤引入，暂不创建。
"""

__version__ = "0.1.0"
