"""端口实现层：适配外部世界。

每个适配器实现一个端口（如 DeepSeek 适配 LLMProvider），互相不 import，
由使用端（api/cli）注入 pipeline。当前为空壳，首个适配器随 Step 0 落地。
"""
