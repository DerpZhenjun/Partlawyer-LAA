@echo off
chcp 65001 >nul
title LabourLawyer 网页端停止器
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\stop-web.ps1"
pause
