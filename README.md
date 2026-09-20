# MoonInsight

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-v4-06B6D4?logo=tailwindcss&logoColor=white)
![shadcn/ui](https://img.shields.io/badge/shadcn/ui-000000?logo=shadcnui&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE4FE7?logo=uv&logoColor=white)
![pnpm](https://img.shields.io/badge/pnpm-F69220?logo=pnpm&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white)
[![CI](https://github.com/Sapphire127/MoonInsight/actions/workflows/ci.yml/badge.svg)](https://github.com/Sapphire127/MoonInsight/actions/workflows/ci.yml)

金融助手 Agent —— 以 AI Agent 形态提供金融助手能力的参考级实现。

## 技术栈

- Python 3.12 + FastAPI + OpenAI SDK（模型是配置项，首例 DeepSeek）
- Next.js 16 + TypeScript（前后端同仓库，dev 代理免 CORS）
- 工具链：uv + pnpm + pytest

## 快速开始

### 初始配置（仅第一次）

```bash
# 后端（app/ 目录）
cd app
cp .env.example .env          # 填入 LLM_API_KEY
uv sync                       # 安装后端依赖

# 前端（web/ 目录）
cd ../web && pnpm install     # 安装前端依赖
```

### 日常运行（每次开发）

```bash
# 后端（app/ 目录）
cd app && uv run --env-file .env uvicorn moon_insight.interfaces.main:app --port 8000

# 前端（另开终端，web/ 目录）
cd web && pnpm dev
# 打开 http://localhost:5173

# 测试（app/ 目录）
cd app && uv run pytest       # fake 注入测试零成本；真实 LLM 测试需配置 LLM_API_KEY

# 端到端测试（web/ 目录，自动拉起前后端）
cd web && pnpm test:e2e
```

## 免责声明

本项目仅用于研究与学习，不构成任何投资建议。
