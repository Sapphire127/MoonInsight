# 框架选型调研（金融助手 Agent · 企业级）

> 定位：按企业级 AI Agent 的常用能力域，逐项调研当前主流技术栈。原则：**每个技术标注引入时机，不提前引入**——先用最小配置跑通，再按需演进。
> 性质：本文件是调研记录 + 推荐，**最终选型须经确认后定案**。需求背景见 `spec.md`。

## 选型总表

| # | 能力域 | 企业常用（调研） | 本项目推荐 |
|---|---|---|---|
| 1 | Agent 编排 | LangGraph / OpenAI Agents SDK / Microsoft Agent Framework / CrewAI | LangGraph（复杂状态工作流时） |
| 2 | LLM 接入 | OpenAI SDK / LiteLLM 网关 | OpenAI SDK 薄封装 + LLMProvider 端口 |
| 3 | 模型 | per-task 可换 | 配置项非选型（首例 DeepSeek，已确认） |
| 4 | 记忆与状态 | 外部检索式记忆 + 分层（episodic/semantic） | DB + 向量索引，治理先行 |
| 5 | RAG / 向量库 | Chroma（原型）→ pgvector/Qdrant → Milvus（十亿级） | Chroma 起步，留端口 |
| 6 | 工具协议 | MCP（de facto 标准，Linux Foundation 治理） | MCP；A2A 暂无多 Agent 不需要 |
| 7 | 金融数据 | Tushare / efinance / akshare / pytdx / baostock | Tushare + efinance 起步 |
| 8 | 后端与流式 | FastAPI + SSE（生产共识） | FastAPI + SSE |
| 9 | 任务调度 | APScheduler（单机）→ Celery（分布式）→ Temporal（长工作流） | APScheduler 起步 |
| 10 | 可观测 | Langfuse（OSS 自托管）/ LangSmith + OTel GenAI 约定 | Langfuse |
| 11 | 评估 | EDD：golden set + promptfoo（CI 门禁）/ DeepEval + LLM-judge | 自研 harness + promptfoo |
| 12 | 治理与安全 | 运行时护栏 + 确定性代码校验 + policy-as-code + 审计 | 确定性校验（混合架构） |
| 13 | 前端 | Next.js App Router + Vercel AI SDK + Tailwind/shadcn | 同左 |
| 14 | 数据库 | SQLite → PostgreSQL；SQLAlchemy + Alembic | 同左 |
| 15 | 部署运维 | Docker Compose → K8s；Prometheus/Grafana | 同左 |

## 各能力域详述

### 1. Agent 编排：LangGraph

- **企业格局**：LangGraph 是「有状态、受监管工作负载」最生产化的开源选择（1.0 GA，企业部署案例：Klarna、Uber、LinkedIn、BlackRock、JPMorgan）；OpenAI Agents SDK 适合单 Agent 少工具的轻量场景（handoff 模式）；Microsoft Agent Framework（AutoGen + Semantic Kernel 合并后 GA）适合 Azure/.NET；CrewAI 是快速原型赛道，团队常在生产复杂度上来后迁移到 LangGraph。
- **选型规则（业界共识）**：按「主导约束」选——每个步骤都要可检查、可恢复 → LangGraph；短对话流 → 供应商 SDK；AutoGen 已进入维护模式，新项目不选。
- **防锁死**：81% 企业领导者担忧供应商依赖；推荐把业务逻辑放在框架无关层。
- **本项目**：先手写循环，复杂度起来再上 LangGraph——与「不提前引入框架」原则一致。

### 2. LLM 接入：OpenAI SDK 薄封装

国内主流 API（DeepSeek 等）几乎全兼容 OpenAI 格式；SDK 自带重试、流式、JSON schema 结构化输出、usage 返回。LiteLLM 网关在需要多供应商 fallback/预算管控时升级引入。保持 LLMProvider 端口，供应商可换。

### 3. 模型：配置项，非选型（盘问第一轮确认）

接口结构已锁定（OpenAI SDK 兼容格式，已锁决策 ①），具体模型是配置值——首例 DeepSeek（已有 key、兼容 OpenAI 格式、结构化输出稳定）。各任务 per-task 可换；「不追最新模型，追可评估」。

### 4. 记忆与状态

- **企业共识**：外部检索式记忆为主（灵活、可治理、可更新），配合 token 级上下文管理；分层：episodic（事件）+ semantic（事实）+ procedural（执行模式）；纯 in-context 不可扩展，fine-tune 更新代价高。
- **治理要点**：每条记忆带来源/时间戳/置信度；作用域隔离；版本与回滚；遗忘权（GDPR）；记忆漂移用权威上下文图定期校验。
- **本项目**：业务扩展后才需要长记忆；数据库存结构化事实，向量索引存语义，治理从第一天设计。

### 5. RAG / 向量库

对比共识：**没有单一最优**，按规模与现有设施选——Chroma（原型/本地，<100K 文档，无 RBAC）；已用 Postgres 且 <50M 向量 → pgvector（唯一带 PITR 与行级安全的 OSS 引擎）；性能敏感/过滤复杂 → Qdrant（Rust，原生混合检索）；十亿级分布式 → Milvus。本项目：Chroma 起步，检索走端口，规模到了换 pgvector/Qdrant。

### 6. 工具协议：MCP

- **已是 de facto 标准**：Anthropic 捐赠给 Linux Foundation 下的 Agentic AI Foundation（OpenAI、Google、Microsoft、AWS 等支持）；97M 月 SDK 下载；9,400+ 公共 server；已是采购基线要求（RFP 常设项）。
- **风险**：2,614 个 server 中 82% 存在路径穿越、67% 代码注入漏洞；需要 RBAC、最小权限、审计。A2A 用于 Agent 间协作，无多 Agent 场景不需要。
- **本项目**：MCP 为框架基础能力（见 spec 盘问第二轮决策）；把端口包装为 MCP server，与内部端口并存。

### 7. 金融数据（A 股）

| 工具 | 特点 | 定位 |
|---|---|---|
| Tushare(Pro) | 国内最规范，token 注册，日线/财务/指数免费 | 行情数据主力 |
| efinance | 免费覆盖广，东财聚合 | 备用适配器 |
| akshare | 零注册但本质是爬虫，易失效/被封，禁 7×24 生产 | 仅本地原型 |
| pytdx | 免费实时 Level1（1–3 秒延迟），逆向协议，个人学习用 | 盘中场景备选 |
| baostock | 纯免费盘后数据，含退市股，无实时 | 回测 |

通用避坑：免费源缺逐笔/Level2；回测需确认复权与退市股；**个人非商业使用尚可，商业使用有合规风险**。

### 8. 后端与流式：FastAPI + SSE

当前生产共识：FastAPI `StreamingResponse` + SSE 帧；异步非阻塞（AsyncOpenAI）；生产要点——反代禁用缓冲（nginx `proxy_buffering off`）、15 秒心跳防 ALB 60s 超时、`request.is_disconnected()` 检测断连并中止上游、流中错误用结构化 error 事件；监控 TTFT、tokens/s。SSE 用于聊天流式，WebSocket 留给双向/语音。

### 9. 任务调度

APScheduler（单机、需持久化 JobStore）→ Celery（分布式默认，Redis broker，注意 beat 单点与投递保证）→ Temporal（持久化工作流，事件溯源，多步骤有顺序/原子性要求时）。决策问句：任务能静默失败吗？失败顺序重要吗？月量级？本项目定时类任务 APScheduler 起步足够，上 Celery 的时机是「多进程/多机 + 任务量」出现时。

### 10. 可观测：Langfuse

OSS 可观测事实标准：MIT、自托管免费、被 ClickHouse 收购后承诺保持 MIT；覆盖 trace/prompt 版本/评估/成本；DACH 企业默认（GDPR 与 EU AI Act 日志合规）。LangSmith 与 LangGraph 集成最顺但 SaaS-only + 按席位计费。配合 OTel GenAI 语义约定。本项目按需引入——质量目标没有 trace 就无法验证。

### 11. 评估：EDD（eval-driven development）

- **主流工作流**：版本化 golden set 做回归基线 → 改 prompt/模型 → 重跑看 delta → 生产 trace 的新边界案例回填 golden set；离线 CI eval（LLM-judge + 人工）+ 在线生产 eval（<50ms 确定性打分 + 抽样深评）。
- **工具**：promptfoo（MIT，CI 门禁 + 红队最强，被 OpenAI 收购）；DeepEval（Agent 场景）；Ragas（RAG 专属）；Langfuse 也可做评估平台。
- **真正的难点不是工具**：是 golden set 的建设与 LLM-judge 校准（judge 有长度/位置/自我偏好偏差）。
- **本项目**：自研 harness 为主（指标集随业务定），promptfoo 做 CI 门禁。

### 12. 治理与安全

- **行业范式转变**：护栏从 prompt 层移到**运行时边界执行**——工具调用前预授权、循环中间检查点、集中控制面；「规则在 prompt 层失效，在边界生效」。
- **混合架构（本项目核心）**：LLM 出 schema 约束的提案，确定性代码层校验后执行（已锁决策 ② 的工程形态）。
- **企业标配**：Agent 作为非人类主体运行（最小权限、短期凭证）；高风险动作人工批准；外部内容视为敌意输入；policy-as-code（Rego/Cedar）版本化独立管理；审计可重建任何一次运行（取了什么数据、调了什么工具、产出了什么）。

### 13. 前端：Next.js + Vercel AI SDK

当前参考栈：Next.js App Router + TypeScript + Tailwind/shadcn + Vercel AI SDK（`streamText` 服务端 / `useChat` 客户端），SSE 分帧、工具调用渲染、provider 一行切换全被 SDK 吸收。

### 14. 数据库

SQLite 零运维起步 → PostgreSQL（需要 pgvector/并发/行级安全时）；SQLAlchemy + Alembic 迁移，切库只改连接串。

### 15. 部署运维

Docker Compose 起步（主服务 + Langfuse + 向量库）；K8s 留到规模化评估。监控 Prometheus + Grafana（TTFT、token 用量、KV-cache 等 LLM 特有指标）。

## 金融场景特有要点

- **合规红线（待确认）**：不预测涨跌、不编造、不输出确定性投资建议。
- **数据合规**：免费数据源个人学习可用；商业用途有版权与合规风险——项目定位须明确。
- **确定性优先原则**：数值计算与校验由代码完成，LLM 出结构化提案（已锁决策 ②）——这是本项目与通用 Agent 模板的差异点，也是对外展示时最有辨识度的部分。

## 调研对照结论（开源项目与文章）

1. **金融 Agent 类项目的共性**：单 Python 包起步（不急着拆）、LangGraph 编排、配置与 env 分离、决策日志/checkpoint 是标配（对应本项目的运行记录）、「研究用途免责」是行业惯例
2. **平台类项目的共性**：前后端同仓库分离（api/ + web/ + docker/）、专项深挖胜过全面铺开、任务队列（Celery）是标配
3. **文章类共性**：monorepo 对 AI agent 有利已成行业共识；AGENTS.md/CLAUDE.md 是仓库约定的事实载体；边界要么程序化执行（Nx tags/lint）要么写成硬规则（multica 的 AGENTS.md）；ADRs 记录布局决策
4. **本项目仓库的分区方式（根层 harness + .scratch 规格 + 顶层包代码）与上述项目一致**：单仓库分区是标准形态，多包分层是规模出现后再做的事

## 参考来源

- [The AI Agent Infrastructure Stack in 2026 (Itexus)](https://itexus.com/the-ai-agent-infrastructure-stack-in-2026-protocols-frameworks-and-models/)
- [The AI stack for enterprise engineering in 2026 (Northflank)](https://northflank.com/blog/ai-stack-for-enterprise-engineering)
- [Best AI agent frameworks and agentic frameworks guide (Dataiku)](https://www.dataiku.com/blog/ai-agent-frameworks)
- [Agentic Framework Selection Guide for Enterprise 2026 (Atlan)](https://atlan.com/know/ai-agent/how-to-choose-agentic-framework-enterprise/)
- [The future of MCP: 2026 roadmap and enterprise adoption (Toloka)](https://toloka.ai/blog/the-future-of-mcp-enterprise-adoption/)
- [Prompt Evaluation: Promptfoo, LangSmith, Langfuse Compared (Blck Alpaca)](https://blckalpaca.at/en/knowledge-base/ai-agents/prompt-engineering-for-agents/prompt-evaluation-frameworks)
- [Top Vector Databases for Enterprise AI: 2026 Comparison (Atlan)](https://atlan.com/know/top-vector-databases-enterprise-ai/)
- [2026年A股数据API怎么选（TickDB）](https://tickdb.ai/blog/general/2026%e5%b9%b4a%e8%82%a1%e6%95%b0%e6%8d%aeapi%e6%80%8e%e4%b9%88%e9%80%89%e5%85%8d%e8%b4%b9%e5%bc%80%e6%ba%90%e5%92%8c%e4%b8%93%e4%b8%9a%e6%95%b0%e6%8d%ae%e6%ba%90%e5%af%b9%e6%af%94%e9%99%84%e7%9c%9f%e5%ae%9e%e8%b0%83%e7%94%a8)
- [Enterprise AI Agent Guardrails: A Compliance Checklist 2026 (Atlan)](https://atlan.com/know/ai-agent/enterprise-ai-agent-guardrails-checklist/)
- [Agent Memory Architectures: 5 Patterns and Trade-offs (Atlan)](https://atlan.com/know/agent-memory-architectures/)
- [Task Queues in Production: Celery vs Temporal vs Native FastAPI (DEV)](https://dev.to/uaslimcreate/task-queues-in-production-celery-vs-temporal-vs-native-fastapi-16hl)
- [Building a Production LLM API Server: FastAPI + vLLM (Prem AI)](https://www.premai.io/blog/building-a-production-llm-api-server-fastapi-vllm-complete-guide-2026/)
- [How to Build an AI Chat App Interface With the Vercel AI SDK (freeCodeCamp)](https://www.freecodecamp.org/news/how-to-build-an-ai-chat-app-interface-with-the-ai-sdk)
