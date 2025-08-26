import re
import json

from bot_utils.screenshot import capture_region, enhanced_screenshot
from bot_core.ocr import extract_text, extract_number
from bot_core.recognizer import match_template

from bot_utils.constants import SUPPORT_CARD_ICON_REGION, MOOD_REGION, TURN_REGION, FAILURE_REGION, YEAR_REGION, MOOD_LIST, CRITERIA_REGION, SKILL_PTS_REGION

is_bot_running = False

MINIMUM_MOOD = None
PRIORITIZE_G1_RACE = None
IS_AUTO_BUY_SKILL = None
SKILL_PTS_CHECK = None
PRIORITY_STAT = None
MAX_FAILURE = None
STAT_CAPS = None
SKILL_LIST = None
CANCEL_CONSECUTIVE_RACE = None

# GUI Configuration
GUI_CONFIG = None
TRAINING_LOGIC = "auto"
RAINBOW_STRICT = True

# Status tracking variables
is_bot_running = False
current_action = "Idle"
skill_buying_status = "Not Active"

def set_gui_config(config):
  """Set GUI configuration for bot use"""
  global GUI_CONFIG, TRAINING_LOGIC, RAINBOW_STRICT, MAX_FAILURE, MINIMUM_MOOD, PRIORITIZE_G1_RACE, CANCEL_CONSECUTIVE_RACE, IS_AUTO_BUY_SKILL
  GUI_CONFIG = config
  
  # Apply GUI settings to bot state
  if config:
    TRAINING_LOGIC = config.get("training_logic", "auto")
    RAINBOW_STRICT = config.get("rainbow_strict", True)
    
    # Map GUI failure chance to bot max failure
    failure_chance = config.get("failure_chance", 20)
    MAX_FAILURE = failure_chance
    
    # Map GUI mood level to bot minimum mood
    mood_level = config.get("minimal_mood", 3)
    mood_mapping = {1: "VERY BAD", 2: "BAD", 3: "NORMAL", 4: "GOOD", 5: "VERY GOOD"}
    MINIMUM_MOOD = mood_mapping.get(mood_level, "NORMAL")
    
    # Apply other GUI settings
    PRIORITIZE_G1_RACE = config.get("prioritize_g1", True)
    CANCEL_CONSECUTIVE_RACE = config.get("cancel_consecutive", False)
    IS_AUTO_BUY_SKILL = config.get("enable_skill_buying", False)
    
    print(f"[GUI] Applied settings: Logic={TRAINING_LOGIC}, Failure={MAX_FAILURE}%, Mood={MINIMUM_MOOD}")

def get_training_logic():
  """Get current training logic setting"""
  return TRAINING_LOGIC

def get_rainbow_strict():
  """Get current rainbow strict mode setting"""
  return RAINBOW_STRICT

def load_config():
  with open("config.json", "r", encoding="utf-8") as file:
    return json.load(file)

def reload_config():
  global PRIORITY_STAT, MINIMUM_MOOD, MAX_FAILURE, PRIORITIZE_G1_RACE, CANCEL_CONSECUTIVE_RACE, STAT_CAPS, IS_AUTO_BUY_SKILL, SKILL_PTS_CHECK, SKILL_LIST
  config = load_config()

  PRIORITY_STAT = config["priority_stat"]
  MINIMUM_MOOD = config["minimum_mood"]
  MAX_FAILURE = config["maximum_failure"]
  PRIORITIZE_G1_RACE = config["prioritize_g1_race"]
  CANCEL_CONSECUTIVE_RACE = config["cancel_consecutive_race"]
  STAT_CAPS = config["stat_caps"]
  IS_AUTO_BUY_SKILL = config["skill"]["is_auto_buy_skill"]
  SKILL_PTS_CHECK = config["skill"]["skill_pts_check"]
  SKILL_LIST = config["skill"]["skill_list"]

# Get Stat
def stat_state():
  # Region coordinates in (left, top, right, bottom) format
  stat_regions = {
    "spd": (310, 723, 310+55, 723+20),    # (310, 723, 365, 743)
    "sta": (405, 723, 405+55, 723+20),    # (405, 723, 460, 743)
    "pwr": (500, 723, 500+55, 723+20),    # (500, 723, 555, 743)
    "guts": (595, 723, 595+55, 723+20),   # (595, 723, 650, 743)
    "wit": (690, 723, 690+55, 723+20)     # (690, 723, 745, 743)
  }

  result = {}
  for stat, region in stat_regions.items():
    img = enhanced_screenshot(region)
    val = extract_number(img)
    result[stat] = val
  return result

# Check support card in each training
def check_support_card(threshold=0.8):
  SUPPORT_ICONS = {
    "spd": "game_assets/icons/support_card_type_spd.png",
    "sta": "game_assets/icons/support_card_type_sta.png",
    "pwr": "game_assets/icons/support_card_type_pwr.png",
    "guts": "game_assets/icons/support_card_type_guts.png",
    "wit": "game_assets/icons/support_card_type_wit.png",
    "friend": "game_assets/icons/support_card_type_friend.png"
  }

  count_result = {}

  for key, icon_path in SUPPORT_ICONS.items():
    matches = match_template(icon_path, SUPPORT_CARD_ICON_REGION, threshold)
    count_result[key] = len(matches)

  return count_result

# Get failure chance (idk how to get energy value)
def check_failure():
  failure = enhanced_screenshot(FAILURE_REGION)
  failure_text = extract_text(failure).lower()

  if not failure_text.startswith("failure"):
    return -1

  # SAFE CHECK
  # 1. If there is a %, extract the number before the %
  match_percent = re.search(r"failure\s+(\d{1,3})%", failure_text)
  if match_percent:
    return int(match_percent.group(1))

  # 2. If there is no %, but there is a 9, extract digits before the 9
  match_number = re.search(r"failure\s+(\d+)", failure_text)
  if match_number:
    digits = match_number.group(1)
    idx = digits.find("9")
    if idx > 0:
      num = digits[:idx]
      return int(num) if num.isdigit() else -1
    elif digits.isdigit():
      return int(digits)  # fallback

  return -1

# Check mood
def check_mood():
  mood = capture_region(MOOD_REGION)
  mood_text = extract_text(mood).upper()

  for known_mood in MOOD_LIST:
    if known_mood in mood_text:
      return known_mood

  print(f"[WARNING] Mood not recognized: {mood_text}")
  return "UNKNOWN"

# Check turn
def check_turn():
    turn = enhanced_screenshot(TURN_REGION)
    turn_text = extract_text(turn)

    if "Race Day" in turn_text:
        return "Race Day"

    # sometimes easyocr misreads characters instead of numbers
    cleaned_text = (
        turn_text
        .replace("T", "1")
        .replace("I", "1")
        .replace("O", "0")
        .replace("S", "5")
    )

    digits_only = re.sub(r"[^\d]", "", cleaned_text)

    if digits_only:
      return int(digits_only)
    
    return -1

# Check year
def check_current_year():
  year = enhanced_screenshot(YEAR_REGION)
  text = extract_text(year)
  return text

# Check criteria
def check_criteria():
  img = enhanced_screenshot(CRITERIA_REGION)
  text = extract_text(img)
  return text

def check_skill_pts():
  img = enhanced_screenshot(SKILL_PTS_REGION)
  text = extract_number(img)
  return text
