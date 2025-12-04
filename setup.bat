@echo off
REM Setup script for Windows - Movie Recommendation System

echo ============================================================
echo   Movie Recommendation System - Windows Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/7] Python detected
python --version

REM Create virtual environment
echo.
echo [2/7] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
    set /p recreate="Do you want to recreate it? (y/N): "
    if /i "%recreate%"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q venv
        python -m venv venv
    )
) else (
    python -m venv venv
)

if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo.
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo [5/7] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Create .env file
echo.
echo [6/7] Setting up environment file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo Created .env file from template
    ) else (
        echo SECRET_KEY=django-insecure-dev-key-change-in-production>.env
        echo DEBUG=True>>.env
        echo ALLOWED_HOSTS=localhost,127.0.0.1>>.env
        echo Created basic .env file
    )
) else (
    echo .env file already exists
)

REM Create logs directory
if not exist logs mkdir logs

REM Run migrations
echo.
echo [7/7] Running database migrations...
python manage.py migrate

if errorlevel 1 (
    echo [WARNING] Database migration failed
)

REM Success message
echo.
echo ============================================================
echo   Setup Complete! 🎉
echo ============================================================
echo.
echo Your Movie Recommendation System is ready!
echo.
echo Next steps:
echo   1. The virtual environment is already activated
echo   2. Run: python manage.py runserver
echo   3. Open: http://localhost:8000
echo.
echo Documentation:
echo   - README.md - Full documentation
echo   - QUICKSTART.md - Quick start guide
echo.
echo Press any key to start the server or Ctrl+C to exit...
pause >nul

python manage.py runserver

