import { expect, test } from "@playwright/test";

// 阶段 ② E2E：无工具调用路径——回答直接渲染，无工具调用 badge。
// fake 后端（DemoLLM）对该问题回放固定直接回答。
test("直接问答渲染回答且无工具调用", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("textbox").fill("FASTAPI是什么？");
  await page.getByRole("button", { name: "发送" }).click();

  await expect(page.getByText("这是脚本化直接回答（fake LLM）。")).toBeVisible();
  await expect(page.getByText("calculator")).toHaveCount(0);
});
