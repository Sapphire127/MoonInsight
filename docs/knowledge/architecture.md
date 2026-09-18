# 仓库布局与架构约定

## 仓库布局（harness 约定）

harness（上下文工程与 spec 资产：约定、规格、决策文档）与正式代码同仓库、分区存放：

- 根层上下文：`CLAUDE.md`（约定单一事实源）、`AGENTS.md`（跨工具指针，内容不重复）、`CONTEXT.md`、`.gitignore`
- 项目级 harness：`.claude/`（`settings.local.json` 为本地个人配置，不入库）
- 约定文档：`docs/agents/`（工作流约定）、`docs/knowledge/`（工程约定与知识库）、`docs/adr/`（重大决策，决策产生时创建）
- SDD 规格资产：`.scratch/<feature>/`（spec、选型、issue，随仓库 push）
- 正式代码（前后端平级，各自为完整项目）：
  - 后端 `app/`：Python 项目（`pyproject.toml` + `src/moon_insight/` 四层 + `_tests_/` + `.env`，src 布局，import `moon_insight.xxx`）
  - 前端 `web/`：Next.js 项目（src/ 布局：`src/app/` 路由壳 + `src/main/` 分层；测试随 `src/_tests_/`）
  - 前后端只经 HTTP/SSE 通信（语言边界即包边界）；根目录只放 harness 与跨项目资产
- 运行产物与密钥（`reports/`、`.env`、`.venv/`、缓存）不入仓库，见 `.gitignore`

## 命名映射（防混用）

品牌与仓库名 CamelCase（MoonInsight）；Python 包 snake_case（`moon_insight`）；打包名与路径 slug kebab-case（`moon-insight`）；CLI 命令全小写无分隔（`mooninsight`）。

## 分区原则

harness 不进源码树、代码里不埋 agent 指令；「怎么干活的约定」在边界层，「干活的产物」在 `src/`。多仓库拆分是组织规模问题，当前不适用。
