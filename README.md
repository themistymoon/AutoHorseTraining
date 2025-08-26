# AutoHorseTraining

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub stars](https://img.shields.io/github/stars/themistymoon/AutoHorseTraining.svg)](https://github.com/themistymoon/AutoHorseTraining/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/themistymoon/AutoHorseTraining.svg)](https://github.com/themistymoon/AutoHorseTraining/issues)

Advanced automated training system for Uma Musume Pretty Derby with sophisticated point-based decision making and configurable hotkey support.

## Attribution & Credits

This project builds upon the excellent work from:
- **Original Repository**: [samsulpanjul/umamusume-auto-train](https://github.com/samsulpanjul/umamusume-auto-train)
- **Template matching inspiration**: [shiokaze/UmamusumeAutoTrainer](https://github.com/shiokaze/UmamusumeAutoTrainer)

### Contributors to the original work:
- **samsulpanjul** - Original author and main developer
- **daftuyda** - Contributing developer  

We are grateful to all contributors who made this project possible.

**USE AT YOUR OWN RISK** - We are not responsible for any issues, account bans, or losses that may occur from using this tool.

## Features

- **Point-Based Training System** with intelligent supporter recognition
- **Configurable Hotkeys** with easy GUI editor (default F1)
- **Modern Overlay GUI** with dark theme and real-time controls
- **Multi-Monitor Support** for dual monitor setups
- **Special Supporter Recognition** (Kitasan, Director, Otonashi)
- **Rainbow Synergy Bonuses** for matching supporter types
- **Mood-Based Recreation Logic** for optimal training efficiency
- **Real-time OCR and Template Matching** for game state detection
- **Automatic Race Handling** with aptitude matching
- **Stat Target System** to prevent overtraining
- **Auto-Purchase Skills** with configurable skill selection

## Requirements

- **Python 3.10 or higher**
- **Windows OS** (tested on Windows 10/11)
- **Screen Resolution:** 1920x1080 (fullscreen game)
- **Uma Musume Pretty Derby** installed and running

## Quick Start

### Option 1: One-Click Launcher (Recommended)
1. Download the latest release ZIP file
2. Extract to any folder
3. **Double-click `AutoHorseTraining.bat`**
4. The launcher will automatically install dependencies and start the GUI

### Option 2: Manual Installation
```bash
git clone https://github.com/themistymoon/AutoHorseTraining.git
cd AutoHorseTraining
pip install -r requirements.txt
python start_gui.py
```

## Usage

### Running the Bot

#### GUI Mode (Recommended)
```bash
python start_gui.py
```
- Modern overlay interface with hotkey support
- Real-time configuration and bot status
- Configurable hotkey system (default F1)
- Dark theme and multi-monitor support

#### Direct Overlay
```bash
python overlay_gui.py
```
- Same features as GUI mode
- Direct launch without startup messages

#### Terminal Mode
```bash
python main.py
```
- Command line interface only
- Uses config.json settings
- F1 hotkey still works

### First Time Setup

1. **Run the GUI:** `python start_gui.py` or `AutoHorseTraining.bat`
2. **Configure Monitor** (for dual monitor users):
   - Go to Monitor Settings section
   - Select monitor where game is running
   - Test with "Test Screenshot" and "Test OCR"
3. **Configure Training:**
   - Set training priorities
   - Configure mood and failure thresholds
   - Set up skill auto-purchase
   - Adjust stat caps

### Hotkey Configuration

- Click the hotkey button (shows current key like "F1") next to "Start Training"
- Press any key in the dialog to set as new hotkey
- Changes take effect immediately and save automatically
- Default is F1, can be changed to any key

## Point-Based Training System

Advanced scoring system that evaluates training options:

### Base Scoring
- **1.0 point** per regular supporter in training
- **1.5 points** for supporters with exclamation marks
- **1.5 points** for Kitasan (special recognition)
- **0.5 points** for Director and Otonashi

### Bonuses
- **+0.5 points** for Speed or Wisdom training (main stats)
- **2.0 points** for matching rainbow supporters
- **5.0 points** when 2+ matching rainbow supporters in same training

### Recreation Logic
- If best training scores less than 2.5-3.0 points AND mood isn't Great, choose recreation

## Game Requirements

- **Screen Resolution:** Must be 1920x1080
- **Game Mode:** Fullscreen only
- **Prerequisites:** Uma must have won trophies for races (bot skips races)
- **Window State:** Game window must not be covered by other applications

## Controls

### In-Game
- **Configurable Hotkey (default F1):** Start/Stop bot toggle
- Works from anywhere while game is active

### GUI Interface
- **Start/Stop:** Large button or hotkey
- **Test Screenshot:** Verify monitor detection
- **Test OCR:** Check text recognition
- **Skills Editor:** Configure auto-purchase
- **Monitor Settings:** Multi-monitor support

### Running the Bot

You now have multiple options to run the bot:

#### Option 1: Overlay GUI (Recommended)
```
python start_gui.py
```

Features:
- Modern overlay interface with hotkey support
- Real-time configuration changes and bot status
- Built-in F1 hotkey for in-game control
- Dark theme and responsive design

#### Option 2: Direct GUI
```
python overlay_gui.py
```
#### Option 3: Terminal Mode
```
python main.py
```

Features:
- Command line interface only
- Uses existing config.json settings
- F1 hotkey still works for start/stop

### BEFORE YOU START

Make sure these conditions are met:

- Screen resolution must be 1920x1080
- The game should be in fullscreen
- Your Uma must have already won the trophy for each race (the bot will skips the race)
- Turn off all confirmation pop-ups in game settings
- The game must be in the career lobby screen (the one with the Tazuna hint icon)

### Start

Run:

```
python main.py
```

Start:
press `f1` to start/stop the bot.

### Configuration

Open your browser and go to: `http://127.0.0.1:8000/` to easily edit the bot's configuration.

### Training Logic

There are 2 training logics used:

1. Train in the area with the most support cards.
2. Train in an area with a rainbow support bonus.

During the first year, the bot will prioritize the first logic to quickly unlock rainbow training.

Starting from the second year, it switches to the second logic. If there’s no rainbow training and the failure chance is still below the threshold, it falls back to the first one.

### Known Issue

- Some Uma that has special event/target goals (like Restricted Train Goldship or 2 G1 Race Oguri Cap) may not working.
- OCR might misread failure chance (e.g., reads 33% as 3%) and proceeds with training anyway.
- Automatically picks the top option during chain events. Be careful with Acupuncture event, it always picks the top option.
- If you bring a friend support card (like Tazuna/Aoi Kiryuin) and do recreation, the bot can't decide whether to date with the friend support card or the Uma.
- When `prioritize_g1_race` is set to `true`, the bot will always prioritize racing, even if your energy is low or you've already done 3 or more consecutive races.

## 📜 License & Attribution

### License
This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

### Original Work License
This project builds upon the original work by [samsulpanjul](https://github.com/samsulpanjul) and other contributors. We respect and maintain the same open-source licensing spirit as the original repository.

### Major Enhancements in This Fork
- ✨ **Advanced Point-Based Training System** with image recognition for special supporters
- 🎯 **Sophisticated Scoring Algorithm** (Kitasan, exclamation marks, rainbow bonuses)
- 🎮 **Modern Overlay GUI** with dark theme and improved UX
- 🖥️ **Multi-Monitor Support** and enhanced screen detection
- 🔧 **Comprehensive Bug Fixes** and improved error handling
- 📁 **Restructured Codebase** for better maintainability

### Acknowledgments
Special thanks to:
- **[samsulpanjul](https://github.com/samsulpanjul)** for creating the original AutoTrain system
- **[daftuyda](https://github.com/daftuyda)** for contributions to the original codebase
- **[shiokaze](https://github.com/shiokaze/UmamusumeAutoTrainer)** for template matching inspiration
- The **Umamusume community** for their continuous support and feedback

---

## ⚠️ Disclaimer

This software is provided "as is" without any warranties. Use at your own risk. We are not responsible for any issues, account bans, or losses that may occur from using this software. Always use responsibly and in accordance with the game's terms of service.

### TODO

- ~~Prioritize G1 races for farm fans~~
- ~~Auto-purchase skills~~
- Automate Claw Machine event
- ~~Add stat target feature, if a stat already hits the target, skip training that one~~

### Contribute

If you run into any issues or something doesn’t work as expected, feel free to open an issue.
Contributions are very welcome! If you want to contribute, please check out the [dev](https://github.com/samsulpanjul/umamusume-auto-train/tree/dev) branch, which is used for testing new features. I truly appreciate any support to help improve this project further.
