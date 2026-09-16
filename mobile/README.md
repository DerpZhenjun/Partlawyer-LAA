# LabourLawyer Android 手机端

手机端通过 Capacitor 复用 `frontend/` 的群众服务页面，生成的是可以安装到 Android 手机的 APK，不是桌面端 Electron 程序。

## USB 调试安装

1. 手机开启“开发者选项”和“USB 调试”，连接电脑后允许本机调试。
2. 双击仓库根目录的 `start-web.bat`，保持网页后端和数字人运行。
3. 双击仓库根目录的 `install-mobile.bat`。脚本会自动完成构建、端口转发、安装和启动。

如果需要手动操作，先执行 `adb devices`，确认设备状态为 `device`，再运行：

   ```powershell
   adb reverse tcp:8000 tcp:8000
   adb reverse tcp:3000 tcp:3000
   ```

然后在本目录执行 `npm install`，再执行 `npm run android:install`，最后在手机上打开“LabourLawyer 劳动仲裁助手”。

调试 APK 位于 `mobile/android/app/build/outputs/apk/debug/app-debug.apk`。

## 正式发布前

将前端的 `VITE_API_BASE_URL` 和 `VITE_DIGITAL_LAWYER_URL` 设置为已备案的 HTTPS 服务地址，重新构建并使用正式签名生成 release APK/AAB。生产版本不应依赖 USB 端口转发或本机 `127.0.0.1`。
