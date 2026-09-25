@echo off
title SmartChoice Launcher
echo ========================================================
echo        SmartChoice Full-Stack Platform Launcher
echo ========================================================
echo.

:: 1. Launch FastAPI Backend in a separate window
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "SmartChoice - Backend (FastAPI)" cmd /k "cd /d D:\SmartChoice\backend && call .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

:: Wait 2 seconds for backend initialization
timeout /t 2 /nobreak >nul

:: 2. Launch Next.js Frontend in a separate window
echo [2/2] Starting Next.js Frontend on http://localhost:3000 ...
start "SmartChoice - Frontend (Next.js)" cmd /k "cd /d D:\SmartChoice\frontend && npm run dev"

:: Wait 3 seconds for Turbopack to spin up
timeout /t 3 /nobreak >nul

:: 3. Automatically launch your browser
echo.
echo Opening SmartChoice in your default browser...
start http://localhost:3000

echo.
echo ========================================================
echo Both servers are running! 
echo Close the respective terminal windows when done.
echo ========================================================
echo.
pause