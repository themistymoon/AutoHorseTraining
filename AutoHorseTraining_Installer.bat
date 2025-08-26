@echo off
title AutoHorseTraining Installer
color 0A
echo ===============================================
echo    AutoHorseTraining Installer v1.0
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version

REM Get installation directory
set "INSTALL_DIR=%USERPROFILE%\AutoHorseTraining"
echo.
echo [2/5] Installation directory: %INSTALL_DIR%

REM Create installation directory
if exist "%INSTALL_DIR%" (
    echo Directory already exists. Updating installation...
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"

echo.
echo [3/5] Copying files...
xcopy /s /e /y "." "%INSTALL_DIR%\" >nul
if errorlevel 1 (
    echo ERROR: Failed to copy files!
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo [4/5] Setting up Python environment...
cd /d "%INSTALL_DIR%"
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

REM Install dependencies
call .venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

REM Create desktop shortcut
echo.
echo [5/5] Creating desktop shortcut...
set "SHORTCUT_PATH=%USERPROFILE%\Desktop\AutoHorseTraining.lnk"
set "TARGET_PATH=%INSTALL_DIR%\AutoHorseTraining.bat"
set "ICON_PATH=%INSTALL_DIR%\game_assets\icon.ico"

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP%\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\shortcut.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP%\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\shortcut.vbs"
echo oLink.Description = "AutoHorseTraining - Automated Horse Training Bot" >> "%TEMP%\shortcut.vbs"
if exist "%ICON_PATH%" echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP%\shortcut.vbs"
echo oLink.Save >> "%TEMP%\shortcut.vbs"

cscript //nologo "%TEMP%\shortcut.vbs"
del "%TEMP%\shortcut.vbs"

REM Create Start Menu shortcut
set "STARTMENU_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\AutoHorseTraining.lnk"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\startmenu.vbs"
echo sLinkFile = "%STARTMENU_PATH%" >> "%TEMP%\startmenu.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\startmenu.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP%\startmenu.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\startmenu.vbs"
echo oLink.Description = "AutoHorseTraining - Automated Horse Training Bot" >> "%TEMP%\startmenu.vbs"
if exist "%ICON_PATH%" echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP%\startmenu.vbs"
echo oLink.Save >> "%TEMP%\startmenu.vbs"

cscript //nologo "%TEMP%\startmenu.vbs"
del "%TEMP%\startmenu.vbs"

echo.
echo ===============================================
echo    Installation Complete!
echo ===============================================
echo.
echo AutoHorseTraining has been installed to:
echo %INSTALL_DIR%
echo.
echo Desktop shortcut created: AutoHorseTraining.lnk
echo Start Menu shortcut created
echo.
echo You can now:
echo - Double-click the desktop shortcut to start
echo - Find it in Start Menu
echo - Run from: %INSTALL_DIR%\AutoHorseTraining.bat
echo.
echo Press any key to launch AutoHorseTraining...
pause >nul

REM Launch the application
start "" "%TARGET_PATH%"

exit /b 0
