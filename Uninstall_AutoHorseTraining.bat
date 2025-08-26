@echo off
title AutoHorseTraining Uninstaller
color 0C
echo ===============================================
echo    AutoHorseTraining Uninstaller
echo ===============================================
echo.

set "INSTALL_DIR=%USERPROFILE%\AutoHorseTraining"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\AutoHorseTraining.lnk"
set "STARTMENU_SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\AutoHorseTraining.lnk"

echo This will remove AutoHorseTraining from your computer.
echo Installation directory: %INSTALL_DIR%
echo.
set /p "CONFIRM=Are you sure you want to uninstall? (y/N): "

if /i not "%CONFIRM%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Removing AutoHorseTraining...

REM Remove shortcuts
if exist "%DESKTOP_SHORTCUT%" (
    del "%DESKTOP_SHORTCUT%"
    echo ✓ Desktop shortcut removed
)

if exist "%STARTMENU_SHORTCUT%" (
    del "%STARTMENU_SHORTCUT%"
    echo ✓ Start Menu shortcut removed
)

REM Remove installation directory
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    echo ✓ Installation directory removed
)

echo.
echo AutoHorseTraining has been successfully uninstalled.
echo.
pause
