import type { NextConfig } from "next";

// 前后端同仓库的开发代理：/api/* 转发到 Python 后端（8000）。
// 浏览器只与前端同 origin 通信，无需 CORS；
// 生产部署时由网关（如 nginx）承担同样的职责。
const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },
};

export default nextConfig;
