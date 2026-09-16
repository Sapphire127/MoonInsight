import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MoonInsight",
  description: "金融助手 Agent —— hello world",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
