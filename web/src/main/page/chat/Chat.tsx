"use client";
import { useState } from "react";
import type { ChatMessage } from "@/main/domain/chat";
import { sendChat } from "@/main/domain/shared/chatClient";

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
    <div className="chat">
      <h1>MoonInsight</h1>
      <div className="chatList">
        {messages.map((m) => (
          <div key={m.id} className={`message ${m.role}`}>
            <div className="content">{m.content}</div>
            {m.toolCalls?.map((tc, i) => (
              <div key={i} className="toolCall">
                工具 {tc.name}（{JSON.stringify(tc.arguments)}）→ {tc.result}
              </div>
            ))}
          </div>
        ))}
      </div>
      <div className="inputRow">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          disabled={busy}
        />
        <button onClick={handleSend} disabled={busy}>
          发送
        </button>
      </div>
    </div>
  );
}
