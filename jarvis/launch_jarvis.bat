@echo off
echo.
echo ==========================================
echo     JARVIS - AI Assistant Launcher
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found!

:: Navigate to script directory
cd /d "%~dp0"

:: Install requirements if needed
echo.
echo Checking dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Starting JARVIS...
echo.

:: Run JARVIS
python main.py

:: Pause on exit
echo.
pause
