@echo off
REM Canteen Token System - GitHub & Cloud Setup

echo.
echo ====================================================
echo   Canteen Token System - Setup for GitHub/Cloud
echo ====================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

echo [OK] Git found

REM Initialize git
if not exist .git (
    echo.
    echo Initializing git repository...
    git init
    echo [OK] Git initialized
)

REM Stage all files
echo.
echo Staging files...
git add .
echo [OK] Files staged

REM Create commit
echo.
echo Creating initial commit...
git commit -m "Initial commit: Two separate apps (Student + Admin/Scanner) with 213 students"
echo [OK] Commit created

REM Display next steps
echo.
echo.
echo ====================================================
echo   NEXT STEPS:
echo ====================================================
echo.
echo 1. Create GitHub repository:
echo    - Go to github.com/new
echo    - Name: canteen-token-system
echo    - Create repository
echo.
echo 2. Connect to GitHub:
echo    git remote add origin https://github.com/YOUR_USERNAME/canteen-token-system.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy Student App to Heroku:
echo    cd student_app
echo    heroku login
echo    heroku create student-canteen-app
echo    git push heroku main
echo.
echo 4. Deploy Admin/Scanner App to Heroku:
echo    cd ..\admin_scanner_app
echo    heroku login
echo    heroku create admin-scanner-app
echo    git push heroku main
echo.
echo ====================================================
echo.
pause
