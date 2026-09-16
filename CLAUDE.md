# MoonInsight

## 语言约定

- 与用户的所有交流使用中文
- 生成的文档使用中文
- 代码、变量命名、commit message 保持英文

## Git 权限

- Agent 无 commit 权限：不执行 `git commit` / `git push`，所有提交由用户手动进行。Agent 完成工作后输出建议的 commit message 供用户参考。

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/` in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage roles, each label string equal to its name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Grilling

需求、计划、选型在动手前必须经过盘问式收敛（设计树 + frontier 轮次），盘问未结束不进入实现；盘问中确认的决策落 spec.md、新术语落 CONTEXT.md、重大决策落 docs/adr/。See `docs/agents/grilling.md`.

## 仓库布局（harness 约定）

harness（上下文工程与 spec 资产：约定、规格、决策文档）与正式代码同仓库、分区存放：

- 根层上下文：`CLAUDE.md`（约定单一事实源）、`AGENTS.md`（跨工具指针，内容不重复）、`CONTEXT.md`、`.gitignore`
- 项目级 harness：`.claude/`（`settings.local.json` 为本地个人配置，不入库）
- 工作流约定：`docs/agents/`；重大决策记录：`docs/adr/`（决策产生时创建）
- SDD 规格资产：`.scratch/<feature>/`（spec、选型、issue，随仓库 push）
- 正式代码：顶层包或 `src/`；`_tests_/` 与代码同版本（前端测试随 web/ 的 `src/_tests_/` 惯例）
- 前端：`web/`（Next.js 体系，src/ 布局：`src/app/` 路由壳 + `src/main/` 分层；与后端只经 HTTP/SSE 通信，语言边界即包边界）
- 运行产物与密钥（`reports/`、`.env`、`.venv/`、缓存）不入仓库，见 `.gitignore`

命名映射（防混用）：品牌与仓库名 CamelCase（MoonInsight）；Python 包 snake_case（`moon_insight`）；打包名与路径 slug kebab-case（`moon-insight`）；CLI 命令全小写无分隔（`mooninsight`）。

分区原则：harness 不进源码树、代码里不埋 agent 指令；「怎么干活的约定」在边界层，「干活的产物」在 `src/`。多仓库拆分是组织规模问题，当前不适用。

## 工程决策原则

一切选型与工程决策兼顾「成品可展示」与「方法论可沉淀」——仓库整体是交付物，决策与过程记录须经得起公开评审；文档措辞公开中立，不落个人敏感意图，需要表达时一律用「可展示性/公开评审」表述。
