# 前端代码规约（web/）

## 文件组织

- 组件文件共置：`.tsx` + 同名小写 `.ts`（辅助方法）+ 私有 hook 放同一目录
- 复杂计算逻辑从组件中抽出，放组件同名的 `.ts` 文件
- 不要按类型跨目录拆分

## 命名规范

| 类别 | 命名方式 | 示例 |
|---|---|---|
| 组件文件 | PascalCase，名词 | `ChatInput.tsx` |
| 组件主函数 | 与文件名相同 | `function ChatInput() {}` |
| 组件辅助文件 | camelCase，名词（与组件同名小写） | `chatInput.ts` |
| 业务方法 | 动词/动名词组 | `getSession()`, `formatMessage()` |
| 纯逻辑文件 | camelCase，名词 | `streamParser.ts` |
| Hook 文件 | use + 名词，camelCase | `useChatStream.ts` |

## TypeScript

- 禁止 any，确有必要标注理由
- 接口用 interface，类型别名用 type
- **枚举提取**：同一语义的字符串字面量出现在 ≥2 处不同位置（跨文件/跨模块）时，提取为 `enum` 放到 `domain/shared/types.ts`；仅单个模块内使用的字面量保留在模块类型文件内。目的：消除魔法字符串、编译期检查拼写

## 类型定义规则

- **domain 层业务类型**：放对应业务模型的 `.ts` 文件（如 `message.ts` 定义消息相关 interface/type）
- **page 层类型**：单组件使用的 Props 写在组件文件内；跨组件使用的提取到 `page/shared/`

## React 组件

- 函数组件 + Hooks
- Props 类型显式定义
- 页面级错误兜底使用 Next.js 的 `error.tsx` / `global-error.tsx` 机制，不手工包 ErrorBoundary

## 分层边界

- `src/app/`：路由壳，不含业务实现
- `src/main/domain/`：纯 TypeScript，不依赖 React；`domain/shared/` 放业务无关基础设施（通信封装、通用工具）——不含展示逻辑
- `src/main/page/`：React 组件 + 私有 hook 共置；`page/shared/` 放跨页面组件与 hook
- **数据流**：page → 通信层/服务 → 后端；page 层不直接手写请求

## 共享级别

- 单个组件内复用 → 放组件同名 `.ts` 文件
- 单个页面内跨组件 → 放页面目录内
- 模块内跨页面 → 放 `page/{Module}/shared/`
- 跨模块 → 放 `page/shared/`（React/TS）或 `domain/shared/`（业务无关）

## 批量修改

跨多个文件（≥3 个）进行同类修改时：

- **优先逐个手动编辑**：先用一个文件验证模式，确认后在其余文件重复相同编辑——文件结构有差异时批量脚本的匹配和修复成本远超手动
- **批量脚本仅在结构高度一致时使用**：至少手动验证过 2 个文件确认模式完全相同后再用
- **保留 git 备份点**：批量修改前确认工作区干净，出问题快速回退

## 样式方案（已定稿）

- **Tailwind CSS v4**（utility-first，PostCSS 插件接入）+ **shadcn/ui**（组件源码进项目）+ OKLCH 设计令牌（`globals.css` 的 CSS 变量体系）
- 基础 UI 组件放 `src/main/page/shared/ui/`（跨模块共享组件）；`cn` 合并工具放 `src/main/page/shared/utils.ts`
- **命名例外**：`page/shared/ui/` 下的 shadcn 组件文件名跟随上游惯例（小写，如 `button.tsx`），导出组件名仍 PascalCase（`Button`）；自有业务组件文件仍按 PascalCase 命名——例外原因：保持与 `npx shadcn add` 生成行为及上游 diff 的一致性
- **组合规则**：间距用 `gap-*` 不用 `space-y-*`；等宽高用 `size-*`；颜色只用语义 token（`bg-primary`、`text-muted-foreground` 等），不写裸色值；暗色模式由 token 自动承载，不手写 `dark:` 覆盖

## 待定（对应设施引入时补规则）

- 状态管理：若引入状态库，补「UI 与状态分离」细则
- 国际化：若启用，采用两级 Key 结构（顶层共享键 + 模块命名空间）
- 表单验证与错误反馈：出现表单场景时补规则
