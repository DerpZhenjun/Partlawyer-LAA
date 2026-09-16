# LabourLawyer Desktop

桌面端复用 `frontend` 构建产物，通过 Electron 提供独立窗口与安装包。开发时先启动 Web：

```bash
cd frontend && npm run dev
cd ../desktop && npm install && npm run dev
```

生产打包执行 `npm run dist`。主进程默认启用上下文隔离、沙箱并禁止 Node 注入；外部链接交给系统浏览器。
