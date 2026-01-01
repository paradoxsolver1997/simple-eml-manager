@echo off
chcp 65001 >nul
title EML Search server
color 0A

echo ========================================
echo        EML Search Server starts
echo ========================================
echo.

REM Set the working directory to the directory where the script is located
cd /d "%~dp0"

REM examinePython
python --version >nul 2>nul
if errorlevel 1 (
    echo [Error] Python not found
    echo Install Python first
    echo Download address: https://www.python.org
    pause
    exit /b 1
)



echo [INFO] Starting up FastAPI server...
echo Front-end interface: http://localhost:8000
echo.
echo Press Ctrl+C to Stop the server
echo ========================================
echo.

call ..\.venv\Scripts\activate.bat && cd .. && uvicorn backend.main:app --reload --port 8000 --host 0.0.0.0

if errorlevel 1 (
    echo [Error] Server startup failed！
    pause
    exit /b 1
)

echo [INFO] Server has stopped
pause



