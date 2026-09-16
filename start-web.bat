@echo off
chcp 65001 >nul
title LabourLawyer 网页端启动器
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-web.ps1" -WithDigitalHuman
if errorlevel 1 (
  echo.
  echo 启动失败，请查看上方提示。
  pause
)
