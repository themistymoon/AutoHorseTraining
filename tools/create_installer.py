#!/usr/bin/env python3
"""
AutoHorseTraining Installer Creator
Creates a Windows installer that sets up the application and creates desktop shortcuts
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_installer_script():
    """Create the installer batch script"""
    installer_content = '''@echo off
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
set "INSTALL_DIR=%USERPROFILE%\\AutoHorseTraining"
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
xcopy /s /e /y "." "%INSTALL_DIR%\\" >nul
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
call .venv\\Scripts\\activate.bat
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

REM Create desktop shortcut
echo.
echo [5/5] Creating desktop shortcut...
set "SHORTCUT_PATH=%USERPROFILE%\\Desktop\\AutoHorseTraining.lnk"
set "TARGET_PATH=%INSTALL_DIR%\\AutoHorseTraining.bat"
set "ICON_PATH=%INSTALL_DIR%\\game_assets\\icon.ico"

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\\shortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP%\\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\shortcut.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP%\\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\shortcut.vbs"
echo oLink.Description = "AutoHorseTraining - Automated Horse Training Bot" >> "%TEMP%\\shortcut.vbs"
if exist "%ICON_PATH%" echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP%\\shortcut.vbs"
echo oLink.Save >> "%TEMP%\\shortcut.vbs"

cscript //nologo "%TEMP%\\shortcut.vbs"
del "%TEMP%\\shortcut.vbs"

REM Create Start Menu shortcut
set "STARTMENU_PATH=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\AutoHorseTraining.lnk"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\\startmenu.vbs"
echo sLinkFile = "%STARTMENU_PATH%" >> "%TEMP%\\startmenu.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\startmenu.vbs"
echo oLink.TargetPath = "%TARGET_PATH%" >> "%TEMP%\\startmenu.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\startmenu.vbs"
echo oLink.Description = "AutoHorseTraining - Automated Horse Training Bot" >> "%TEMP%\\startmenu.vbs"
if exist "%ICON_PATH%" echo oLink.IconLocation = "%ICON_PATH%" >> "%TEMP%\\startmenu.vbs"
echo oLink.Save >> "%TEMP%\\startmenu.vbs"

cscript //nologo "%TEMP%\\startmenu.vbs"
del "%TEMP%\\startmenu.vbs"

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
echo - Run from: %INSTALL_DIR%\\AutoHorseTraining.bat
echo.
echo Press any key to launch AutoHorseTraining...
pause >nul

REM Launch the application
start "" "%TARGET_PATH%"

exit /b 0
'''
    
    with open('AutoHorseTraining_Installer.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("✅ Created AutoHorseTraining_Installer.bat")

def create_icon():
    """Create a simple icon file (placeholder - you can replace with actual icon)"""
    icon_dir = Path("game_assets")
    icon_dir.mkdir(exist_ok=True)
    
    # Create a simple text file as placeholder icon
    # In a real scenario, you'd want to use a proper .ico file
    icon_path = icon_dir / "icon.ico"
    if not icon_path.exists():
        # Create a minimal placeholder - in practice, use a proper icon editor
        with open(icon_path, 'w') as f:
            f.write("# AutoHorseTraining Icon Placeholder\n")
        print("⚠️  Created placeholder icon - replace with actual .ico file")

def create_uninstaller():
    """Create an uninstaller script"""
    uninstaller_content = '''@echo off
title AutoHorseTraining Uninstaller
color 0C
echo ===============================================
echo    AutoHorseTraining Uninstaller
echo ===============================================
echo.

set "INSTALL_DIR=%USERPROFILE%\\AutoHorseTraining"
set "DESKTOP_SHORTCUT=%USERPROFILE%\\Desktop\\AutoHorseTraining.lnk"
set "STARTMENU_SHORTCUT=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\AutoHorseTraining.lnk"

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
'''
    
    with open('Uninstall_AutoHorseTraining.bat', 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    print("✅ Created Uninstall_AutoHorseTraining.bat")

def create_exe_installer():
    """Create a self-extracting exe installer using PyInstaller"""
    try:
        # Check if PyInstaller is installed
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', 'pyinstaller'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("📦 Installing PyInstaller...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        
        # Create installer Python script
        installer_py_content = '''
import os
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import winreg

class AutoHorseTrainingInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoHorseTraining Installer")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        self.install_dir = Path.home() / "AutoHorseTraining"
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2d3748", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="AutoHorseTraining", 
                              font=("Arial", 18, "bold"), fg="white", bg="#2d3748")
        title_label.pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        tk.Label(main_frame, text="Welcome to AutoHorseTraining Installer", 
                font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        tk.Label(main_frame, text="This will install AutoHorseTraining on your computer.", 
                wraplength=400).pack(pady=(0, 20))
        
        # Installation directory
        dir_frame = tk.Frame(main_frame)
        dir_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(dir_frame, text="Installation Directory:").pack(anchor="w")
        self.dir_var = tk.StringVar(value=str(self.install_dir))
        dir_entry = tk.Entry(dir_frame, textvariable=self.dir_var, width=50)
        dir_entry.pack(fill="x", pady=(5, 0))
        
        # Options
        options_frame = tk.LabelFrame(main_frame, text="Options", padx=10, pady=10)
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.desktop_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Create desktop shortcut", 
                      variable=self.desktop_var).pack(anchor="w")
        
        self.startmenu_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Add to Start Menu", 
                      variable=self.startmenu_var).pack(anchor="w")
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=(0, 10))
        
        self.status_label = tk.Label(main_frame, text="Ready to install", fg="green")
        self.status_label.pack()
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        tk.Button(button_frame, text="Cancel", command=self.root.quit).pack(side="right", padx=(10, 0))
        self.install_btn = tk.Button(button_frame, text="Install", command=self.install, 
                                   bg="#4299e1", fg="white", font=("Arial", 10, "bold"))
        self.install_btn.pack(side="right")
    
    def update_status(self, text):
        self.status_label.config(text=text)
        self.root.update()
    
    def install(self):
        try:
            self.install_btn.config(state="disabled")
            self.progress.start()
            
            self.update_status("Checking Python installation...")
            if not self.check_python():
                messagebox.showerror("Error", "Python 3.8+ is required but not found.\\nPlease install Python from https://python.org")
                return
            
            self.update_status("Creating installation directory...")
            self.install_dir = Path(self.dir_var.get())
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            self.update_status("Extracting files...")
            self.extract_files()
            
            self.update_status("Setting up Python environment...")
            self.setup_environment()
            
            if self.desktop_var.get():
                self.update_status("Creating desktop shortcut...")
                self.create_desktop_shortcut()
            
            if self.startmenu_var.get():
                self.update_status("Adding to Start Menu...")
                self.create_startmenu_shortcut()
            
            self.progress.stop()
            self.update_status("Installation complete!")
            
            messagebox.showinfo("Success", f"AutoHorseTraining has been installed to:\\n{self.install_dir}\\n\\nYou can now launch it from the desktop shortcut or Start Menu.")
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Installation Error", f"An error occurred during installation:\\n{str(e)}")
            self.install_btn.config(state="normal")
    
    def check_python(self):
        try:
            result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def extract_files(self):
        # This would extract the embedded files in a real installer
        # For now, just copy the current directory
        import shutil
        current_dir = Path(__file__).parent
        for item in current_dir.iterdir():
            if item.name not in ['installer.py', '__pycache__']:
                if item.is_dir():
                    shutil.copytree(item, self.install_dir / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, self.install_dir)
    
    def setup_environment(self):
        os.chdir(self.install_dir)
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
        
        # Install dependencies
        venv_python = self.install_dir / '.venv' / 'Scripts' / 'python.exe'
        subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    
    def create_desktop_shortcut(self):
        self.create_shortcut(
            Path.home() / "Desktop" / "AutoHorseTraining.lnk",
            self.install_dir / "AutoHorseTraining.bat",
            "AutoHorseTraining - Automated Horse Training Bot"
        )
    
    def create_startmenu_shortcut(self):
        startmenu_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        self.create_shortcut(
            startmenu_dir / "AutoHorseTraining.lnk",
            self.install_dir / "AutoHorseTraining.bat",
            "AutoHorseTraining - Automated Horse Training Bot"
        )
    
    def create_shortcut(self, shortcut_path, target_path, description):
        import tempfile
        
        vbs_content = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_path}"
oLink.WorkingDirectory = "{self.install_dir}"
oLink.Description = "{description}"
oLink.Save
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
            f.write(vbs_content)
            vbs_path = f.name
        
        subprocess.run(['cscript', '//nologo', vbs_path], check=True)
        os.unlink(vbs_path)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = AutoHorseTrainingInstaller()
    installer.run()
'''
        
        with open('installer.py', 'w', encoding='utf-8') as f:
            f.write(installer_py_content)
        
        print("📦 Creating Windows executable installer...")
        subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--windowed',
            '--name', 'AutoHorseTraining_Setup',
            '--icon', 'game_assets/icon.ico' if Path('game_assets/icon.ico').exists() else None,
            'installer.py'
        ], check=True)
        
        print("✅ Created AutoHorseTraining_Setup.exe in dist/ folder")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating exe installer: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 AutoHorseTraining Installer Creator")
    print("=" * 50)
    
    create_icon()
    create_installer_script()
    create_uninstaller()
    
    print("\n📋 Created installer files:")
    print("• AutoHorseTraining_Installer.bat - Simple batch installer")
    print("• Uninstall_AutoHorseTraining.bat - Uninstaller")
    
    choice = input("\n❓ Do you want to create a Windows .exe installer? (y/N): ").strip().lower()
    if choice == 'y':
        create_exe_installer()
    
    print("\n✅ Installer creation complete!")
    print("\n📖 Usage:")
    print("1. Run AutoHorseTraining_Installer.bat for simple installation")
    print("2. Or distribute AutoHorseTraining_Setup.exe for professional installation")
    print("3. Users can uninstall using Uninstall_AutoHorseTraining.bat")

if __name__ == "__main__":
    main()
