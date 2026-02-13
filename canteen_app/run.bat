@echo off
echo ========================================
echo   Canteen Token System - Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [✓] Python found

REM Check if requirements are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [✓] Dependencies installed
)

echo.
echo ========================================
echo   Starting Canteen Token System...
echo ========================================
echo.

python app.py

pause
