@echo off
chcp 65001 >nul
title LabourLawyer Android 安装器
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\install-mobile.ps1"
if errorlevel 1 (
  echo.
  echo 安装没有完成，请按上方提示检查手机连接。
  pause
  exit /b 1
)
echo.
echo 安装完成，手机端已打开。
pause
