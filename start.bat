@echo off
:: 强制开启 UTF-8 编码，防止中文显示乱码
chcp 65001 >nul
title PartLawyer 全栈系统一键启动器
echo =================================================
echo       正在启动 PartLawyer 数字化律师系统...
echo =================================================

:: 设置统一的 Conda 环境名称
set CONDA_ENV=pl

:: 1. 启动 GPT-SoVITS 语音服务
echo [1/4] 启动语音接口...
start "GPT-SoVITS" cmd /k "chcp 65001 >nul && conda activate %CONDA_ENV% && cd GPT-SoVITS && python api_v2.py"

:: 等待 5 秒，确保语音服务先起来
timeout /t 5 /nobreak >nul

:: 2. 启动 FastAPI 后端服务 (使用 app.py 作为入口)
echo [2/4] 启动法律业务后端...
:: 这里已修改为 app:app
start "Backend" cmd /k "chcp 65001 >nul && conda activate %CONDA_ENV% && cd backend && uvicorn app:app --reload --port 8000"

:: 3. 启动前端 Vue 项目
echo [3/4] 启动 Web 前端...
start "Frontend-Vue" cmd /k "chcp 65001 >nul && conda activate %CONDA_ENV% && cd frontend && npm run dev"

:: 4. 启动 ChatVRM 数字人
echo [4/4] 启动数字人组件...
start "ChatVRM" cmd /k "chcp 65001 >nul && conda activate %CONDA_ENV% && cd ChatVRM && npm run dev"

echo =================================================
echo       启动指令已全部发送！
echo       请检查四个弹出的窗口，确保没有报错。
echo =================================================
pause