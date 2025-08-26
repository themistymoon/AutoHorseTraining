#!/usr/bin/env python3
"""
AutoHorseTraining - GUI Launcher
Starts the overlay GUI with F1 hotkey support
"""

import tkinter as tk
from overlay_gui import TrainingAssistant

def main():
    """Launch the training assistant overlay with F1 hotkey support"""
    print("🎯 Starting AutoHorseTraining GUI...")
    print("✅ F1 hotkey will be enabled for in-game control")
    print("💡 Use the overlay or press F1 in-game to start/stop training")
    
    root = tk.Tk()
    app = TrainingAssistant(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        app.close_application()

if __name__ == "__main__":
    main()
