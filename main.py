import time
import pygetwindow as gw
import threading
import keyboard
import pyautogui

from bot_core.execute import career_lobby, career_lobby_iteration
import bot_core.state as state

hotkey = "f1"

def focus_umamusume():
  try:
    win = gw.getWindowsWithTitle("Umamusume")
    target_window = next((w for w in win if w.title.strip() == "Umamusume"), None)
    if target_window.isMinimized:
      target_window.restore()
    else:
      target_window.minimize()
      time.sleep(0.2)
      target_window.restore()
      time.sleep(0.5)
  except Exception as e:
    print(f"Error focusing window: {e}")
    return False
  return True

def main():
  print("Uma Auto!")
  if focus_umamusume():
    state.reload_config()
    career_lobby()
  else:
    print("Failed to focus Umamusume window")

def main_loop(is_running_callback=None):
  """Main bot loop that can be controlled externally"""
  
  # Run the main loop with external control
  if is_running_callback:
    print("Uma Auto!")
    if not focus_umamusume():
      print("Failed to focus Umamusume window")
      return
    
    state.reload_config()
    state.is_bot_running = True
    
    while is_running_callback():
      try:
        # Run one iteration of the career lobby
        career_lobby_iteration()
        if not is_running_callback():
          break
        time.sleep(0.1)  # Small delay between iterations
      except Exception as e:
        print(f"Bot error: {e}")
        break
    state.is_bot_running = False
  else:
    print("Uma Auto!")
    if focus_umamusume():
      state.reload_config()
      career_lobby()
    else:
      print("Failed to focus Umamusume window")

def hotkey_listener():
  while True:
    keyboard.wait(hotkey)
    if not state.is_bot_running:
      print("[BOT] Starting...")
      state.is_bot_running = True
      t = threading.Thread(target=main, daemon=True)
      t.start()
    else:
      print("[BOT] Stopping...")
      state.is_bot_running = False
    time.sleep(0.5)

if __name__ == "__main__":
  threading.Thread(target=hotkey_listener, daemon=True).start()
  # Note: start_server() removed - use overlay GUI instead
  print("[INFO] Use 'python start_gui.py' to launch the overlay GUI")
  print(f"[INFO] Or press '{hotkey}' to start/stop the bot directly")
  
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("\n[INFO] Exiting...")
