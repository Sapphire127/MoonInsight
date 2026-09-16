# MoonInsight

## 语言约定

- 与用户的所有交流使用中文
- 生成的文档使用中文
- 代码、变量命名、commit message 保持英文

## Git 权限

- Agent 无 commit 权限：不执行 `git commit` / `git push`，所有提交由用户手动进行。Agent 完成工作后输出建议的 commit message 供用户参考。

## 约定分文件维护

本文件只保留最高频的全局约定；其余约定按主题分布，禁止堆叠回本文件。

- 工程执行规范与决策原则：`docs/knowledge/conventions.md`
- 代码规范（三大硬约束、执行四准则、审查对照）：`docs/knowledge/code-style.md`
- 前端代码规约（文件组织、命名、分层、共享级别）：`docs/knowledge/frontend-conventions.md`
- 仓库布局、命名映射、分区原则：`docs/knowledge/architecture.md`
- 工作流约定：`docs/agents/`——issue 管理见 `issue-tracker.md`、triage 角色见 `triage-labels.md`、领域文档约定见 `domain.md`、盘问式收敛见 `grilling.md`（需求、计划、选型在动手前必须经盘问收敛，盘问未结束不进入实现）
- 领域词汇：`CONTEXT.md`
- 规格与决策资产：`.scratch/<feature>/`
