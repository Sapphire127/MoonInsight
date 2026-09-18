"""基础设施层（端口实现）：适配外部世界。

每个实现对应领域端口抽象（如 DeepSeekLLM 实现 LLMProvider），
互相不 import，由 interfaces 组装后注入 application。
"""
