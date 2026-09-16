"use client";

import { useEffect, useState } from "react";

// hello world：验证前端 → dev 代理 → 后端的完整调用链。
// 后续真实交互（聊天/流式）在此页迭代或按 features/ 重组。
export default function Home() {
  const [message, setMessage] = useState("loading...");

  useEffect(() => {
    fetch("/api/hello")
      .then((r) => r.json())
      .then((d) => setMessage(d.message))
      .catch(() => setMessage("backend unreachable"));
  }, []);

  return (
    <main>
      <h1>MoonInsight</h1>
      <p>backend says: {message}</p>
    </main>
  );
}
