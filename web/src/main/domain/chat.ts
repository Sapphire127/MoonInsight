// 聊天领域类型（frontend-conventions：domain 层业务类型放对应模型文件）

export interface ToolCallRecord {
  name: string;
  arguments: Record<string, unknown>;
  result: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCallRecord[];
}

export interface ChatResponse {
  final_answer: string;
  tool_calls: ToolCallRecord[];
}
