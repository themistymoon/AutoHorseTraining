import keyboard
import threading
import time
import bot_core.state as state
from main import main_loop, focus_umamusume

class HotkeyManager:
    def __init__(self, overlay_app=None):
        self.overlay_app = overlay_app
        self.is_listening = False
        self.current_hotkey = "f1"  # Default hotkey
        
    def start_hotkey_listener(self):
        """Start the hotkey listener"""
        if not self.is_listening:
            self.is_listening = True
            hotkey_thread = threading.Thread(target=self._hotkey_loop, daemon=True)
            hotkey_thread.start()
            
    def stop_hotkey_listener(self):
        """Stop the hotkey listener"""
        self.is_listening = False
        
    def _hotkey_loop(self):
        """Main hotkey listener loop"""
        print(f"[HOTKEY] {self.current_hotkey.upper()} hotkey listener started")
        
        while self.is_listening:
            try:
                keyboard.wait(self.current_hotkey)
                time.sleep(0.1)  # Debounce
                
                if self.overlay_app:
                    # If overlay is available, toggle through overlay
                    if not self.overlay_app.bot_running:
                        print("[HOTKEY] Starting bot via F1...")
                        self.overlay_app.root.after(0, self.overlay_app.start_bot)
                    else:
                        print("[HOTKEY] Stopping bot via F1...")
                        self.overlay_app.root.after(0, self.overlay_app.stop_bot)
                else:
                    # Fallback to direct control
                    if not state.is_bot_running:
                        print("[HOTKEY] Starting bot...")
                        state.is_bot_running = True
                        bot_thread = threading.Thread(target=self._run_bot_standalone, daemon=True)
                        bot_thread.start()
                    else:
                        print("[HOTKEY] Stopping bot...")
                        state.is_bot_running = False
                        
                time.sleep(0.5)  # Prevent rapid toggling
                
            except Exception as e:
                print(f"[HOTKEY] Error: {e}")
                time.sleep(1)
                
    def _run_bot_standalone(self):
        """Run bot without overlay"""
        try:
            if focus_umamusume():
                state.reload_config()
                main_loop(lambda: state.is_bot_running)
            else:
                print("Failed to focus Umamusume window")
                state.is_bot_running = False
        except Exception as e:
            print(f"Bot error: {e}")
            state.is_bot_running = False

# Global hotkey manager instance
hotkey_manager = None

def start_global_hotkeys(overlay_app=None):
    """Start global hotkey system"""
    global hotkey_manager
    hotkey_manager = HotkeyManager(overlay_app)
    hotkey_manager.start_hotkey_listener()
    
def stop_global_hotkeys():
    """Stop global hotkey system"""
    global hotkey_manager
    if hotkey_manager:
        hotkey_manager.stop_hotkey_listener()
