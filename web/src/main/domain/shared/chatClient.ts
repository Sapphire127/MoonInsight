// 通信层：页面组件不直接手写 fetch（frontend-conventions 数据流规则）
import type { ChatResponse } from "@/main/domain/chat";

export async function sendChat(message: string): Promise<ChatResponse> {
  const resp = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!resp.ok) {
    throw new Error(`chat request failed: ${resp.status}`);
  }
  return (await resp.json()) as ChatResponse;
}
