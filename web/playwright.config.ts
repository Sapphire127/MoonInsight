import { defineConfig } from "@playwright/test";

// E2E：自动拉起前端（5174）+ fake 后端（8001），跑完自动收。
// 前端经 MOON_INSIGHT_BACKEND_URL 代理到 fake 后端——真实 HTTP 完整链路，
// LLM 由脚本化 DemoLLM 回放（MOON_INSIGHT_LLM=fake），确定性且零 API 成本。
// 端口刻意避开开发环境（5173/8000），互不冲突、互不复用。
export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  use: {
    baseURL: "http://localhost:5174",
  },
  webServer: [
    {
      command: "npx next dev -p 5174",
      url: "http://localhost:5174",
      reuseExistingServer: false,
      env: {
        MOON_INSIGHT_BACKEND_URL: "http://localhost:8001",
      },
    },
    {
      command: "cd ../app && .venv/bin/uvicorn moon_insight.interfaces.main:app --port 8001",
      url: "http://localhost:8001/api/hello",
      reuseExistingServer: false,
      env: {
        MOON_INSIGHT_LLM: "fake",
      },
    },
  ],
});
