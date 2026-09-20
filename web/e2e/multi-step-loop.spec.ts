import { expect, test } from "@playwright/test";

// 阶段 ② E2E：多步工具调用路径——两个 calculator badge 与最终回答渲染。
// fake 后端（DemoLLM）对该问题回放两轮 calculator 调用后作答。
test("多步工具调用渲染 calculator badge", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("textbox").fill("先计算 (3+5)*2，再把结果除以 4");
  await page.getByRole("button", { name: "发送" }).click();

  await expect(page.getByText("结果是 4")).toBeVisible();
  await expect(page.getByText('{"expression":"(3+5)*2"}')).toBeVisible();
  await expect(page.getByText('{"expression":"16/4"}')).toBeVisible();
  await expect(page.getByText("16", { exact: true })).toBeVisible();
  await expect(page.getByText("4", { exact: true })).toBeVisible();
});
