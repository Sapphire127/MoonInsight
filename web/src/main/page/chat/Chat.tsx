"use client";

// 聊天界面：阶段 ① 的最小前后端联动（普通 JSON，流式待拍板后升级）
import { useState } from "react";

import type { ChatMessage } from "@/main/domain/chat";
import { sendChat } from "@/main/domain/shared/chatClient";
import { Button } from "@/main/page/shared/ui/button";
import { Card, CardContent } from "@/main/page/shared/ui/card";
import { Input } from "@/main/page/shared/ui/input";

export function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSend() {
    const text = input.trim();
    if (!text || busy) return;
    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role: "user", content: text },
    ]);
    setInput("");
    setBusy(true);
    try {
      const resp = await sendChat(text);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: resp.final_answer,
          toolCalls: resp.tool_calls.length > 0 ? resp.tool_calls : undefined,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "assistant", content: "后端不可达" },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-4 p-6">
      <h1 className="text-xl font-semibold">MoonInsight</h1>
      <div className="flex flex-col gap-2">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <Card
              className={`max-w-[80%] ${m.role === "user" ? "bg-primary/10" : ""}`}
            >
              <CardContent>
                <p>{m.content}</p>
                {m.toolCalls?.map((tc, i) => (
                  <p key={i} className="mt-1 text-xs text-muted-foreground">
                    工具 {tc.name}（{JSON.stringify(tc.arguments)}）→ {tc.result}
                  </p>
                ))}
              </CardContent>
            </Card>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          disabled={busy}
        />
        <Button onClick={handleSend} disabled={busy}>
          发送
        </Button>
      </div>
    </div>
  );
}
