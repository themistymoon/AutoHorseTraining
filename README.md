# AutoHorseTraining - Umamusume Auto Train

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub stars](https://img.shields.io/github/stars/themistymoon/AutoHorseTraining.svg)](https://github.com/themistymoon/AutoHorseTraining/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/themistymoon/AutoHorseTraining.svg)](https://github.com/themistymoon/AutoHorseTraining/issues)

Like the title says, this is a simple auto training for Umamusume with advanced point-based training system.

## 🙏 Attribution & Credits

This project is inspired by and builds upon the excellent work from:
- **Original Repository**: [samsulpanjul/umamusume-auto-train](https://github.com/samsulpanjul/umamusume-auto-train)
- **Template matching inspiration**: [shiokaze/UmamusumeAutoTrainer](https://github.com/shiokaze/UmamusumeAutoTrainer)

### Contributors to the original work:
- **samsulpanjul** - Original author and main developer
- **daftuyda** - Contributing developer  

We are grateful to all the contributors who made this project possible through their hard work and dedication.

---

**Demo video**: Coming soon

**Screenshot**: Coming soon

# ⚠️ USE IT AT YOUR OWN RISK ⚠️

I am not responsible for any issues, account bans, or losses that may occur from using it.
Use responsibly and at your own discretion.

## Features

- Automatically trains Uma
- Keeps racing until fan count meets the goal, and always picks races with matching aptitude
- Checks mood
- Handle debuffs
- Rest
- Prioritizes G1 races if available for fan farming
- Stat target feature, if a stat already hits the target, skip training that one
- Auto-purchase skill
- **Beautiful Overlay GUI** that displays on top of the game
- **F1 Hotkey Support** for easy in-game control
- **Modern Dark Theme** interface
- **Multi-Monitor Support** with easy monitor selection
- **Real-time OCR and Template Matching** for game state detection

## Getting Started

### Quick Start
1. **Double-click `start_bot.bat`** - This will launch the overlay GUI
2. **OR run manually:** `python overlay_gui.py`

### First Time Setup
1. **Configure Monitor** (for dual monitor users):
   - Open the overlay GUI
   - Go to **🖥️ Monitor Settings** section
   - Select the monitor where your game is running
   - Test with **📸 Test Screenshot** and **🔍 Test OCR**

2. **Configure Bot Settings** in the GUI:
   - Set training priorities
   - Configure mood and failure thresholds  
   - Set up skill auto-purchase
   - Adjust stat caps

### Usage
- **Start/Stop Bot:** Press **F1** in-game or use GUI buttons
- **Monitor Status:** Check the overlay for real-time bot status
- **Adjust Settings:** Modify configuration in the GUI (auto-saves)

### Requirements

- [Python 3.10+](https://www.python.org/downloads/)

### Setup

#### Clone repository

```
git clone https://github.com/samsulpanjul/umamusume-auto-train.git
cd umamusume-auto-train
```

#### Install dependencies

```
pip install -r requirements.txt
```

### Running the Bot

You now have multiple options to run the bot:

#### Option 1: GUI Application (Recommended)
```
python launcher.py
```
Then select option 1 for the desktop GUI application.

Features:
- Visual interface with tabs for different settings
- Real-time configuration changes
- Built-in bot start/stop controls
- No need for web browser

#### Option 2: Web Interface
```
python launcher.py
```
Then select option 2 for the web interface, or run directly:
```
python main.py
```

Features:
- Browser-based configuration at http://localhost:8000
- Good for remote configuration
- Modern web interface

#### Option 3: Hotkey Only
```
python launcher.py
```
Then select option 3 for hotkey-only mode.

Features:
- No configuration interface
- Uses existing config.json
- Press F1 in-game to start/stop

#### Quick Start (Windows)
Double-click `start_bot.bat` for an easy launcher.

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
