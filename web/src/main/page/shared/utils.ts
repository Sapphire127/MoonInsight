// 跨组件共享工具（frontend-conventions：跨模块 TS 工具 → page/shared/）
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
