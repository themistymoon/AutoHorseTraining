import pyautogui
import Levenshtein
import sys
import os

# Add bot_utils to path for mouse utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bot_utils'))

try:
    from mouse_utils import smart_move_and_click, smart_move_to
    USE_SMART_MOUSE = True
except ImportError:
    USE_SMART_MOUSE = False

from monitor_manager import monitor_manager
from bot_utils.screenshot import enhanced_screenshot
from bot_core.ocr import extract_text
from bot_core.recognizer import match_template, is_btn_active
import bot_core.state as state

def buy_skill():
  # Set status for detection
  state.skill_buying_status = "Scanning for skills..."
  
  # Convert monitor-relative coordinates to absolute screen coordinates
  abs_x, abs_y = monitor_manager.monitor_to_screen_coords(560, 680)
  
  if USE_SMART_MOUSE:
    smart_move_to(abs_x, abs_y)
  else:
    pyautogui.moveTo(x=abs_x, y=abs_y)
    
  found = False

  for _ in range(10):
    state.skill_buying_status = f"Searching skills... (attempt {_+1}/10)"
    buy_skill_icon = match_template("game_assets/icons/buy_skill.png", threshold=0.9)

    if buy_skill_icon:
      for x, y, w, h in buy_skill_icon:
        # Fix coordinate calculation to prevent 'right' < 'left' error
        left = max(0, x - 420)  # Ensure left edge is not negative
        top = max(0, y - 40)    # Ensure top edge is not negative
        width = min(w + 275, 1920 - left)  # Ensure width doesn't exceed screen
        height = min(h + 5, 1080 - top)    # Ensure height doesn't exceed screen
        
        # Only proceed if we have valid dimensions
        if width > 0 and height > 0:
          region = (left, top, width, height)
          try:
            screenshot = enhanced_screenshot(region)
            text = extract_text(screenshot)
            if is_skill_match(text, state.SKILL_LIST):
              button_region = (x, y, w, h)
              if is_btn_active(button_region):
                print(f"[INFO] Buy {text}")
                state.skill_buying_status = f"Purchasing: {text}"
                if USE_SMART_MOUSE:
                    smart_move_and_click(x + 5, y + 5)
                else:
                    pyautogui.click(x=x + 5, y=y + 5, duration=0.15)
                found = True
              else:
                print(f"[INFO] {text} found but not enough skill points.")
                state.skill_buying_status = f"Insufficient points for: {text}"
          except Exception as e:
            print(f"[WARNING] Skill detection error: {e}")

    for _ in range(7):  # Use _ instead of i for unused variable
      pyautogui.scroll(-300)

  # Reset status when done
  if found:
    state.skill_buying_status = "Purchase completed"
  else:
    state.skill_buying_status = "No skills purchased"
    
  return found

def is_skill_match(text: str, skill_list: list[str], threshold: float = 0.75) -> bool:
  for skill in skill_list:
    similarity = Levenshtein.ratio(text.lower(), skill.lower())
    if similarity >= threshold:
      return True
  return False
