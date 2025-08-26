# Build Tools

This folder contains development tools for creating releases and installers.

## Tools Overview

### 🔧 create_installer.py
Creates professional Windows installers for AutoHorseTraining.

**Usage:**
```bash
cd tools
python create_installer.py
```

**Creates:**
- `AutoHorseTraining_Installer.bat` - Simple batch installer
- `Uninstall_AutoHorseTraining.bat` - Uninstaller
- `AutoHorseTraining_Setup.exe` - Professional GUI installer (in dist/ folder)

### 📦 create_release.py
Creates portable ZIP packages for distribution.

**Usage:**
```bash
cd tools
python create_release.py
```

**Creates:**
- `AutoHorseTraining-Release.zip` - Portable version (no installation required)

## Release Process

To create a complete release:

1. **Create installer packages:**
   ```bash
   cd tools
   python create_installer.py
   ```

2. **Create portable package:**
   ```bash
   cd tools
   python create_release.py
   ```

3. **Upload to GitHub Release:**
   - `dist/AutoHorseTraining_Setup.exe` - Recommended installer
   - `AutoHorseTraining-Release.zip` - Portable alternative

## Distribution Options

### For End Users:
- **Recommended:** `AutoHorseTraining_Setup.exe` - Professional installer with GUI
- **Alternative:** `AutoHorseTraining-Release.zip` - Extract and run, no installation
- **Simple:** `AutoHorseTraining_Installer.bat` - Command-line installer

### Features Comparison:
| Feature | Setup.exe | Release.zip | Installer.bat |
|---------|-----------|-------------|---------------|
| GUI Installer | ✅ | ❌ | ❌ |
| Desktop Shortcut | ✅ | ❌ | ✅ |
| Start Menu | ✅ | ❌ | ✅ |
| Auto Environment | ✅ | ❌ | ✅ |
| Portable | ❌ | ✅ | ❌ |
| Size | ~10MB | ~5MB | ~2MB |
