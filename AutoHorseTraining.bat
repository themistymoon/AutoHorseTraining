@echo off
title AutoHorseTraining Launcher
echo AutoHorseTraining - Uma Musume Auto Trainer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import cv2, easyocr, keyboard, pygetwindow" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting AutoHorseTraining GUI...
echo.
echo Controls:
echo - Use the overlay GUI to configure settings
echo - Press F1 in-game to start/stop the bot
echo - Close this window to exit
echo.

python start_gui.py

echo.
echo AutoHorseTraining has closed.
pause
