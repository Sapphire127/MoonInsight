"""金融助手 Agent —— 顶层包。

分包骨架（方案 A）：ports / domain / adapters / pipeline / api / schemas。
依赖方向：api（使用端）→ pipeline → ports → domain；adapters 实现 ports，
由使用端注入。eval / observability / mcp / cli 随步骤引入，暂不创建。
"""

__version__ = "0.1.0"
