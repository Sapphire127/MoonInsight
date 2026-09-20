import type { NextConfig } from "next";

// 前后端同仓库的开发代理：/api/* 转发到 Python 后端（默认 8000，
// 可用 MOON_INSIGHT_BACKEND_URL 覆盖——E2E 时指向 fake 后端 8001）。
// 浏览器只与前端同 origin 通信，无需 CORS；
// 生产部署时由网关（如 nginx）承担同样的职责。
const backendUrl = process.env.MOON_INSIGHT_BACKEND_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
