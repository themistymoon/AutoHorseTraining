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

## Installation

### Quick Start (Windows)
1. Download the repository as ZIP or clone it
2. **Double-click `AutoHorseTraining.bat`** - This will automatically:
   - Check if Python is installed
   - Install required dependencies
   - Start the GUI with hotkey support

### Manual Installation
```bash
git clone https://github.com/themistymoon/AutoHorseTraining.git
cd AutoHorseTraining
pip install -r requirements.txt
```

### Download Release (Coming Soon)
Pre-built executable releases will be available for easier installation.

## Usage

### Running the Bot

#### GUI Mode (Recommended)
```bash
python start_gui.py
```
Features:
- Modern overlay interface with configurable hotkey support
- Real-time configuration and bot status monitoring
- Dark theme optimized for gaming
- Multi-monitor support for dual screen setups

#### Direct Overlay
```bash
python overlay_gui.py
```
Same functionality as GUI mode, just direct launch without startup messages.

#### Terminal Mode
```bash
python main.py
```
Features:
- Command line interface only
- Uses existing config.json settings
- Hotkey functionality still available

### First Time Setup

1. **Start the GUI**: Run `python start_gui.py`

2. **Configure Monitor** (for multi-monitor users):
   - Navigate to Monitor Settings section in the GUI
   - Select the monitor where your game is running
   - Use "Test Screenshot" and "Test OCR" to verify detection

3. **Configure Training Settings**:
   - Set training priority order
   - Configure mood and failure thresholds
   - Enable/disable skill auto-purchase
   - Adjust stat caps to prevent overtraining

4. **Set Your Hotkey**:
   - Click the hotkey button next to "Start Training" (shows current key like "F1")
   - Press any key in the dialog to set as your new hotkey
   - Changes take effect immediately and save automatically

## Point-Based Training System

Advanced scoring system that intelligently evaluates training options:

### Base Scoring
- **1.0 point** per regular supporter in training
- **1.5 points** for supporters with exclamation marks (high motivation)
- **1.5 points** for Kitasan (special supporter recognition)
- **0.5 points** for Director and Otonashi (lower priority supporters)

### Stat Priority Bonuses
- **+0.5 points** for Speed or Wisdom training (prioritizes main stats)

### Rainbow Synergy Bonuses
- **2.0 points** for matching rainbow supporters in their specialized training
- **5.0 points** when 2 or more matching rainbow supporters are in the same training

### Recreation Logic
- If the best available training scores less than 2.5-3.0 points AND current mood isn't "Great", the bot will choose recreation instead to improve mood

## Game Requirements

### Technical Requirements
- **Screen Resolution:** Must be 1920x1080
- **Game Mode:** Fullscreen only
- **Prerequisites:** Uma must have won trophies for available races (bot will skip races)
- **Window State:** Game window must be visible and not covered by other applications

### Setup Requirements
- Make sure the game is running in fullscreen at 1920x1080 resolution
- Your Uma character should have already completed the available races
- Close or minimize other applications that might cover the game window

## Controls

### Hotkey Controls
- **Configurable Hotkey (default F1):** Toggle bot start/stop from anywhere
- **ESC:** Emergency stop (when using GUI)

### GUI Interface
- **Start/Stop Button:** Large green button to control bot execution
- **Hotkey Button:** Click to configure your preferred hotkey
- **Test Screenshot:** Verify the bot can capture your game screen
- **Test OCR:** Check if text recognition is working properly
- **Skills Editor:** Configure which skills to auto-purchase
- **Monitor Settings:** Select correct monitor for multi-monitor setups

## Troubleshooting

### Common Issues

**Bot doesn't detect the game:**
- Ensure game is running in fullscreen at 1920x1080
- Try the "Test Screenshot" button to verify screen capture
- For multi-monitor setups, configure the correct monitor in settings

**OCR not working:**
- Use "Test OCR" button to verify text recognition
- Make sure game language matches expected settings
- Ensure game window is not covered by other applications

**Hotkey not responding:**
- Try changing the hotkey using the GUI button
- Make sure no other applications are capturing the same key
- Restart the GUI if hotkey stops working

**Training decisions seem wrong:**
- Check the point-based system scoring in real-time via GUI
- Verify supporter recognition is working correctly
- Adjust mood and failure thresholds in settings

## Development

### Project Structure
```
AutoHorseTraining/
├── bot_core/           # Core bot logic and state management
├── bot_utils/          # Utility functions for screenshot, OCR
├── game_assets/        # Template images for game recognition
├── start_gui.py        # Main GUI launcher
├── overlay_gui.py      # Overlay interface implementation
├── main.py            # Terminal mode launcher
├── hotkey_manager.py   # Configurable hotkey system
├── config.json        # Bot configuration file
└── requirements.txt    # Python dependencies
```

### Contributing
We welcome contributions! Please feel free to submit issues and pull requests.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Demo and Screenshots

Coming soon - demo video and screenshots will be added to showcase the bot in action.
