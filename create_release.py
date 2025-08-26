#!/usr/bin/env python3
"""
AutoHorseTraining Release Setup
Creates a portable release package
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_release():
    """Create a release package"""
    print("Creating AutoHorseTraining release package...")
    
    # Create release directory
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy essential files
    files_to_copy = [
        "AutoHorseTraining.bat",
        "start_gui.py",
        "overlay_gui.py", 
        "main.py",
        "hotkey_manager.py",
        "monitor_manager.py",
        "config.json",
        "requirements.txt",
        "README.md",
        "LICENSE",
        "CREDITS.md"
    ]
    
    # Copy directories
    dirs_to_copy = [
        "bot_core",
        "bot_utils", 
        "game_assets"
    ]
    
    print("Copying files...")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (not found)")
    
    print("Copying directories...")
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, release_dir / dir_name)
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (not found)")
    
    # Create ZIP file
    zip_path = "AutoHorseTraining-Release.zip"
    print(f"Creating {zip_path}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    # Cleanup
    shutil.rmtree(release_dir)
    
    print(f"Release package created: {zip_path}")
    print("\nRelease includes:")
    print("- AutoHorseTraining.bat (one-click launcher)")
    print("- All core Python files")
    print("- Game assets and configuration")
    print("- Documentation")
    print("\nUsers only need to:")
    print("1. Extract the ZIP file")
    print("2. Double-click AutoHorseTraining.bat")

if __name__ == "__main__":
    create_release()
