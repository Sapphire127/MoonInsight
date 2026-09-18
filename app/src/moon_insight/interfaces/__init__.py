"""接口层（交付与组装）：FastAPI 路由 + 请求 DTO。

前后端同仓库：前端 web/ 经 dev 代理把 /api/* 转发到本服务（见
architecture.md 布局约定），无需 CORS。唯一的组装点——把
infrastructure 实现注入 application。流式（SSE 等）待拍板。
"""
