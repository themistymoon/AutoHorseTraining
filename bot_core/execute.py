import pyautogui
import time
import sys
import os
from PIL import ImageGrab
from monitor_manager import monitor_manager

# Add bot_utils to path for mouse and config utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bot_utils'))

try:
    from mouse_utils import smart_move_and_click, smart_move_to
    from human_behavior import human_behavior
    USE_SMART_MOUSE = True
    USE_HUMAN_BEHAVIOR = True
except ImportError:
    print("Warning: mouse_utils or human_behavior not available, using default pyautogui")
    USE_SMART_MOUSE = False
    USE_HUMAN_BEHAVIOR = False

pyautogui.useImageNotFoundException(False)

import bot_core.state as state
from bot_core.state import check_support_card, check_failure, check_turn, check_mood, check_current_year, check_criteria, check_skill_pts
from bot_core.logic import do_something
from bot_utils.constants import MOOD_LIST
from bot_core.recognizer import is_btn_active, match_template, multi_match_templates
from bot_utils.scenario import ura
from bot_core.skill import buy_skill

templates = {
  "event": "game_assets/icons/event_choice_1.png",
  "inspiration": "game_assets/buttons/inspiration_btn.png",
  "next": "game_assets/buttons/next_btn.png",
  "cancel": "game_assets/buttons/cancel_btn.png",
  "tazuna": "game_assets/ui/tazuna_hint.png",
  "infirmary": "game_assets/buttons/infirmary_btn.png",
  "retry": "game_assets/buttons/retry_btn.png"
}

def click(img: str = None, confidence: float = 0.8, minSearch:float = 2, click: int = 1, text: str = "", boxes = None):
  if not state.is_bot_running:
    return False

  # Add human thinking delay before action
  if USE_HUMAN_BEHAVIOR:
    human_behavior.add_micro_break()

  if boxes:
    if isinstance(boxes, list):
      if len(boxes) == 0:
        return False
      box = boxes[0]
    else :
      box = boxes

    if text:
      print(text)
    x, y, w, h = box
    
    # Convert monitor-relative coordinates to absolute screen coordinates
    abs_x, abs_y = monitor_manager.monitor_to_screen_coords(x, y)
    center = (abs_x + w // 2, abs_y + h // 2)
    
    # Add human-like delay before clicking
    if USE_HUMAN_BEHAVIOR:
      delay = human_behavior.get_human_delay(0.3, 0.1)
      time.sleep(delay)
    
    if USE_SMART_MOUSE:
        smart_move_and_click(center[0], center[1], clicks=click)
    else:
        pyautogui.moveTo(center[0], center[1], duration=0.175)
        pyautogui.click(clicks=click)
    return True

  if img is None:
    return False

  btn = pyautogui.locateCenterOnScreen(img, confidence=confidence, minSearchTime=minSearch)
  if btn:
    if text:
      print(text)
    if USE_SMART_MOUSE:
        smart_move_and_click(btn.x, btn.y, clicks=click)
    else:
        pyautogui.moveTo(btn, duration=0.175)
        pyautogui.click(clicks=click)
    return True
  
  return False

def go_to_training():
  # Try the alternative training button first (since it has more matches)
  if click("game_assets/buttons/training_btn2.png", confidence=0.7, text="[INFO] Found training_btn2.png"):
    return True
  
  # Try the original training button
  if click("game_assets/buttons/training_btn.png", confidence=0.7, text="[INFO] Found training_btn.png"):
    return True
  
  # If neither button clicked successfully, let's see what training-related elements are detected
  screen = monitor_manager.get_screenshot()
  training_matches = multi_match_templates({
    "training_btn": "game_assets/buttons/training_btn.png",
    "training_btn2": "game_assets/buttons/training_btn2.png"
  }, screen=screen, threshold=0.7)
  
  # Try to click training_btn2 first, then training_btn
  if training_matches['training_btn2']:
    if click(boxes=training_matches['training_btn2'][:1], text="[INFO] Clicking training button"):
      return True
  
  if training_matches['training_btn']:
    if click(boxes=training_matches['training_btn'][:1], text="[INFO] Clicking training button"):
      return True
  
  return False

def check_training():
  training_types = {
    "spd": "game_assets/icons/train_spd.png",
    "sta": "game_assets/icons/train_sta.png",
    "pwr": "game_assets/icons/train_pwr.png",
    "guts": "game_assets/icons/train_guts.png",
    "wit": "game_assets/icons/train_wit.png"
  }
  results = {}

  for key, icon_path in training_types.items():
    pos = pyautogui.locateCenterOnScreen(icon_path, confidence=0.8)
    if pos:
      pyautogui.moveTo(pos, duration=0.1)
      pyautogui.mouseDown()
      support_counts = check_support_card()
      total_support = sum(support_counts.values())
      failure_chance = check_failure()
      results[key] = {
        "support": support_counts,
        "total_support": total_support,
        "failure": failure_chance
      }
      print(f"[{key.upper()}] → {support_counts}, Fail: {failure_chance}%")
      time.sleep(0.1)
  
  pyautogui.mouseUp()
  click(img="game_assets/buttons/back_btn.png")
  return results

def do_train(train):
  # Use our template matching system instead of PyAutoGUI's locateCenterOnScreen
  train_icon_path = f"game_assets/icons/train_{train}.png"
  
  # Find training icon using template matching
  try:
    train_matches = match_template(train_icon_path, threshold=0.8)
    
    if train_matches:
      # Get the first match
      x, y, w, h = train_matches[0]
      
      # Convert to absolute screen coordinates
      abs_x, abs_y = monitor_manager.monitor_to_screen_coords(x, y)
      center = (abs_x + w // 2, abs_y + h // 2)
      
      print(f"[INFO] Clicking {train} training at {center}")
      pyautogui.tripleClick(center, interval=0.1, duration=0.2)
    else:
      print(f"[WARNING] Could not find {train} training icon using template matching")
      # Fallback to PyAutoGUI method
      train_btn = pyautogui.locateCenterOnScreen(train_icon_path, confidence=0.8)
      if train_btn:
        print(f"[DEBUG] Found {train} using PyAutoGUI at {train_btn}")
        pyautogui.tripleClick(train_btn, interval=0.1, duration=0.2)
      else:
        print(f"[ERROR] Could not find {train} training icon at all")
  except Exception as e:
    print(f"[ERROR] do_train exception: {e}")
    raise

def do_rest():
  rest_btn = pyautogui.locateCenterOnScreen("game_assets/buttons/rest_btn.png", confidence=0.8)
  rest_summber_btn = pyautogui.locateCenterOnScreen("game_assets/buttons/rest_summer_btn.png", confidence=0.8)

  if rest_btn:
    pyautogui.moveTo(rest_btn, duration=0.15)
    pyautogui.click(rest_btn)
  elif rest_summber_btn:
    pyautogui.moveTo(rest_summber_btn, duration=0.15)
    pyautogui.click(rest_summber_btn)

def do_recreation():
  recreation_btn = pyautogui.locateCenterOnScreen("game_assets/buttons/recreation_btn.png", confidence=0.8)
  recreation_summer_btn = pyautogui.locateCenterOnScreen("game_assets/buttons/rest_summer_btn.png", confidence=0.8)

  if recreation_btn:
    pyautogui.moveTo(recreation_btn, duration=0.15)
    pyautogui.click(recreation_btn)
  elif recreation_summer_btn:
    pyautogui.moveTo(recreation_summer_btn, duration=0.15)
    pyautogui.click(recreation_summer_btn)

def do_race(prioritize_g1 = False):
  click(img="game_assets/buttons/races_btn.png", minSearch=10)  

  consecutive_cancel_btn = pyautogui.locateCenterOnScreen("game_assets/buttons/cancel_btn.png", minSearchTime=0.7, confidence=0.8)
  if state.CANCEL_CONSECUTIVE_RACE and consecutive_cancel_btn:
    click(img="game_assets/buttons/cancel_btn.png", text="[INFO] Already raced 3+ times consecutively. Cancelling race and doing training.")
    return False
  elif not state.CANCEL_CONSECUTIVE_RACE and consecutive_cancel_btn:
    click(img="game_assets/buttons/ok_btn.png", minSearch=0.7)

  time.sleep(0.7)
  found = race_select(prioritize_g1=prioritize_g1)
  if not found:
    print("[INFO] No race found.")
    return False

  race_prep()
  time.sleep(1)
  after_race()
  return True

def race_day():
  click(img="game_assets/buttons/race_day_btn.png", minSearch=10)
  
  click(img="game_assets/buttons/ok_btn.png")
  time.sleep(0.5)

  for i in range(2):
    click(img="game_assets/buttons/race_btn.png", minSearch=2)
    time.sleep(0.5)

  race_prep()
  time.sleep(1)
  after_race()

def race_select(prioritize_g1 = False):
  # Convert monitor-relative coordinates to absolute screen coordinates
  abs_x, abs_y = monitor_manager.monitor_to_screen_coords(560, 680)
  pyautogui.moveTo(x=abs_x, y=abs_y)

  time.sleep(0.2)

  if prioritize_g1:
    print("[INFO] Looking for G1 race.")
    for i in range(2):
      race_card = match_template("game_assets/ui/g1_race.png", threshold=0.9)

      if race_card:
        for x, y, w, h in race_card:
          # Convert monitor-relative region to absolute screen coordinates for PyAutoGUI
          abs_x, abs_y = monitor_manager.monitor_to_screen_coords(x, y)
          # Ensure region coordinates are valid and within screen bounds
          region_width = min(310, 1920 - abs_x) if abs_x >= 0 else 310
          region_height = min(90, 1080 - abs_y) if abs_y >= 0 else 90
          
          # Only proceed if we have valid coordinates
          if abs_x >= 0 and abs_y >= 0 and region_width > 0 and region_height > 0:
            region = (abs_x, abs_y, region_width, region_height)
            match_aptitude = pyautogui.locateCenterOnScreen("game_assets/ui/match_track.png", confidence=0.8, minSearchTime=0.7, region=region)
          else:
            # Skip this region if coordinates are invalid
            continue
          if match_aptitude:
            print("[INFO] G1 race found.")
            pyautogui.moveTo(match_aptitude, duration=0.2)
            pyautogui.click()
            for i in range(2):
              click(img="game_assets/buttons/race_btn.png")
              time.sleep(0.5)
            return True
      
      for i in range(4):
        pyautogui.scroll(-300)
    
    return False
  else:
    print("[INFO] Looking for race.")
    for i in range(4):
      match_aptitude = pyautogui.locateCenterOnScreen("game_assets/ui/match_track.png", confidence=0.8, minSearchTime=0.7)
      if match_aptitude:
        print("[INFO] Race found.")
        pyautogui.moveTo(match_aptitude, duration=0.2)
        pyautogui.click(match_aptitude)

        for i in range(2):
          click(img="game_assets/buttons/race_btn.png")
          time.sleep(0.5)
        return True
      
      for i in range(4):
        pyautogui.scroll(-300)
    
    return False

def race_prep():
  view_result_btn = pyautogui.locateCenterOnScreen("game_assets/buttons/view_results.png", confidence=0.8, minSearchTime=10)
  if view_result_btn:
    pyautogui.click(view_result_btn)
    time.sleep(0.5)
    for i in range(3):
      pyautogui.tripleClick(interval=0.2)
      time.sleep(0.5)

def after_race():
  click(img="game_assets/buttons/next_btn.png", minSearch=5)
  time.sleep(0.3)
  pyautogui.click()
  click(img="game_assets/buttons/next2_btn.png", minSearch=5)

def auto_buy_skill():
  if check_skill_pts() < state.SKILL_PTS_CHECK:
    return

  click(img="game_assets/buttons/skills_btn.png")
  print("[INFO] Buying skills")
  time.sleep(0.5)

  if buy_skill():
    click(img="game_assets/buttons/confirm_btn.png", minSearch=0.5)
    click(img="game_assets/buttons/learn_btn.png", minSearch=0.5)
    time.sleep(0.5)
    click(img="game_assets/buttons/close_btn.png", minSearch=2)
    time.sleep(0.5)
    click(img="game_assets/buttons/back_btn.png")
  else:
    print("[INFO] No matching skills found. Going back.")
    click(img="game_assets/buttons/back_btn.png")

def career_lobby_iteration():
  """Run one iteration of the career lobby logic"""
  if not state.is_bot_running:
    return False
    
  screen = monitor_manager.get_screenshot()
  matches = multi_match_templates(templates, screen=screen)

  if click(boxes=matches["event"], text="[INFO] Event found, selecting top choice."):
    return True
  if click(boxes=matches["inspiration"], text="[INFO] Inspiration found."):
    return True
  if click(boxes=matches["next"]):
    return True
  if click(boxes=matches["cancel"]):
    return True
  if click(boxes=matches["retry"]):
    return True

  if not matches["tazuna"]:
    print("[INFO] Should be in career lobby.")
    return True

  if matches["infirmary"]:
    if is_btn_active(matches["infirmary"][0]):
      click(boxes=matches["infirmary"][0], text="[INFO] Character debuffed, going to infirmary.")
      return True

  mood = check_mood()
  mood_index = MOOD_LIST.index(mood)
  minimum_mood = MOOD_LIST.index(state.MINIMUM_MOOD)
  turn = check_turn()
  year = check_current_year()
  criteria = check_criteria()
  year_parts = year.split(" ")

  print("\n=======================================================================================\n")
  print(f"Year: {year}")
  print(f"Mood: {mood}")
  print(f"Turn: {turn}\n")

  # URA SCENARIO
  if year == "Finale Season" and turn == "Race Day":
    print("[INFO] URA Finale")
    if state.IS_AUTO_BUY_SKILL:
      auto_buy_skill()
    ura()
    for _ in range(2):
      if click(img="game_assets/buttons/race_btn.png", minSearch=2):
        time.sleep(0.5)
    
    race_prep()
    time.sleep(1)
    after_race()
    return True

  # If calendar is race day, do race
  if turn == "Race Day" and year != "Finale Season":
    print("[INFO] Race Day.")
    if state.IS_AUTO_BUY_SKILL and year_parts[0] != "Junior":
      auto_buy_skill()
    race_day()
    return True

  # Mood check
  if mood_index < minimum_mood:
    print("[INFO] Mood is low, trying recreation to increase mood")
    do_recreation()
    return True

  # Check if goals is not met criteria AND it is not Pre-Debut AND turn is less than 10 AND Goal is already achieved
  if criteria.split(" ")[0] != "criteria" and year != "Junior Year Pre-Debut" and turn < 10 and criteria != "Goal Achievedl":
    race_found = do_race()
    if race_found:
      return True
    else:
      # If there is no race matching to aptitude, go back and do training instead
      click(img="game_assets/buttons/back_btn.png", minSearch=1, text="[INFO] Race not found. Proceeding to training.")
      time.sleep(0.5)

  # If Prioritize G1 Race is true, check G1 race every turn
  if state.PRIORITIZE_G1_RACE and year_parts[0] != "Junior" and len(year_parts) > 3 and year_parts[3] not in ["Jul", "Aug"]:
    g1_race_found = do_race(state.PRIORITIZE_G1_RACE)
    if g1_race_found:
      return True
    else:
      # If there is no G1 race, go back and do training
      click(img="game_assets/buttons/back_btn.png", minSearch=1, text="[INFO] G1 race not found. Proceeding to training.")
      time.sleep(0.5)

  # Check training button
  if not go_to_training():
    print("[INFO] Training button is not found.")
    return True

  # Last, do training
  time.sleep(0.5)
  results_training = check_training()
  
  training_logic = state.get_training_logic()
  best_training = do_something(results_training, training_logic)
  
  if best_training == "recreation":
    do_recreation()
  elif best_training:
    go_to_training()
    time.sleep(0.5)
    do_train(best_training)
  else:
    do_rest()
  time.sleep(1)
  
  return True

def career_lobby():
  # Program start
  while state.is_bot_running:
    if not career_lobby_iteration():
      break
