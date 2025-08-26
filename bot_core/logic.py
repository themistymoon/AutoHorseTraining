import bot_core.state as state
from bot_core.state import check_current_year, stat_state

# Helper function to get max failure with default
def get_max_failure():
  return state.MAX_FAILURE if state.MAX_FAILURE is not None else 20

# Helper function to safely get rainbow supporter count
def safe_get_rainbow_count(data, stat):
  """Safely get rainbow supporter count from training data"""
  support_data = data.get("support", {})
  if not isinstance(support_data, dict):
    return 0
  return support_data.get(stat, 0)

# Get priority stat from config
def get_stat_priority(stat_key: str) -> int:
  if state.PRIORITY_STAT is None:
    # Default priority order if not set
    default_priority = ["SPD", "STA", "PWR", "GUTS", "WIT"]
    return default_priority.index(stat_key.upper()) if stat_key.upper() in default_priority else 999
  return state.PRIORITY_STAT.index(stat_key) if stat_key in state.PRIORITY_STAT else 999

# Will do train with the most support card
# Used in the first year (aim for rainbow)
def most_support_card(results):
  # Default max failure if state not set
  max_failure = get_max_failure()
  
  # Seperate wit
  wit_data = results.get("wit")

  # Get all training but wit
  non_wit_results = {
    k: v for k, v in results.items()
    if k != "wit" and int(v["failure"]) <= max_failure
  }

  # Check if train is bad
  all_others_bad = len(non_wit_results) == 0

  if all_others_bad and wit_data and int(wit_data["failure"]) <= max_failure and wit_data["total_support"] >= 2:
    print("\n[INFO] All trainings are unsafe, but WIT is safe and has enough support cards.")
    return "wit"

  filtered_results = {
    k: v for k, v in results.items() if int(v["failure"]) <= max_failure
  }

  if not filtered_results:
    print("\n[INFO] No safe training found. All failure chances are too high.")
    return None

  # Best training
  best_training = max(
    filtered_results.items(),
    key=lambda x: (
      x[1]["total_support"],
      -get_stat_priority(x[0])  # priority decides when supports are equal
    )
  )

  best_key, best_data = best_training

  if best_data["total_support"] <= 1:
    if int(best_data["failure"]) == 0:
      # WIT must be at least 2 support cards
      if best_key == "wit":
        print("\n[INFO] Only 1 support and it's WIT. Skipping.")
        return None
      print(f"\n[INFO] Only 1 support but 0% failure. Prioritizing based on priority list: {best_key.upper()}")
      return best_key
    else:
      print("\n[INFO] Low value training (only 1 support). Choosing to rest.")
      return None

  print(f"\nBest training: {best_key.upper()} with {best_data['total_support']} support cards and {best_data['failure']}% fail chance")
  return best_key

# Do rainbow training
def rainbow_training(results):
  # Get rainbow training
  rainbow_candidates = {
    stat: data for stat, data in results.items()
    if int(data["failure"]) <= get_max_failure() and safe_get_rainbow_count(data, stat) > 0
  }

  if not rainbow_candidates:
    print("\n[INFO] No rainbow training found under failure threshold.")
    return None

  # Find support card rainbow in training
  best_rainbow = max(
    rainbow_candidates.items(),
    key=lambda x: (
      x[1]["support"].get(x[0], 0),
      -get_stat_priority(x[0])
    )
  )

  best_key, best_data = best_rainbow
  print(f"\n[INFO] Rainbow training selected: {best_key.upper()} with {best_data['support'][best_key]} rainbow supports and {best_data['failure']}% fail chance")
  return best_key

def filter_by_stat_caps(results, current_stats):
  # Handle case when STAT_CAPS is not set
  if state.STAT_CAPS is None:
    return results  # No filtering if stat caps not set
  
  return {
    stat: data for stat, data in results.items()
    if current_stats.get(stat, 0) < state.STAT_CAPS.get(stat, 1200)
  }

# Training logic: Strict stat priority
def stat_priority_training(results):
  """Follow stat priority order strictly"""
  # Filter by failure rate
  safe_trainings = {
    stat: data for stat, data in results.items()
    if int(data["failure"]) <= get_max_failure()
  }
  
  if not safe_trainings:
    print("\n[INFO] No safe training found for stat priority mode.")
    return None
  
  # Follow priority order
  for priority_stat in state.PRIORITY_STAT:
    if priority_stat in safe_trainings:
      data = safe_trainings[priority_stat]
      print(f"\n[INFO] Stat priority training: {priority_stat.upper()} with {data['total_support']} support cards and {data['failure']}% fail chance")
      return priority_stat
  
  print("\n[INFO] No priority stat available for training.")
  return None

# Training logic: Rainbow only
def rainbow_only_training(results, strict=True):
  """Only do rainbow training (support type matches training type)"""
  max_failure = get_max_failure()
  rainbow_candidates = {
    stat: data for stat, data in results.items()
    if int(data["failure"]) <= max_failure and safe_get_rainbow_count(data, stat) > 0
  }

  if rainbow_candidates:
    # Choose best rainbow training
    best_rainbow = max(
      rainbow_candidates.items(),
      key=lambda x: (
        safe_get_rainbow_count(x[1], x[0]),  # Rainbow support count
        x[1]["total_support"],         # Total support count
        -get_stat_priority(x[0])       # Priority as tiebreaker
      )
    )

    best_key, best_data = best_rainbow
    rainbow_count = safe_get_rainbow_count(best_data, best_key)
    print(f"\n[INFO] Rainbow only training: {best_key.upper()} with {rainbow_count} rainbow supports and {best_data['failure']}% fail chance")
    return best_key
  
  # No rainbow training available
  if strict:
    print("\n[INFO] No rainbow training found. Strict mode: resting.")
    return None
  else:
    print("\n[INFO] No rainbow training found. Falling back to most support card.")
    return most_support_card(results)

# Training logic: Balanced
def balanced_training(results):
  """Equal priority for all stats, choose safest training"""
  safe_trainings = {
    stat: data for stat, data in results.items()
    if int(data["failure"]) <= get_max_failure()
  }
  
  if not safe_trainings:
    print("\n[INFO] No safe training found for balanced mode.")
    return None
  
  # Choose training with best safety and support combination
  best_training = max(
    safe_trainings.items(),
    key=lambda x: (
      x[1]["total_support"],    # Support count (higher is better)
      -int(x[1]["failure"])     # Failure rate (lower is better)
    )
  )
  
  best_key, best_data = best_training
  print(f"\n[INFO] Balanced training: {best_key.upper()} with {best_data['total_support']} support cards and {best_data['failure']}% fail chance")
  return best_key

# Training logic: Point-based system
def point_based_training(results):
  """Advanced point-based training system with supporter recognition"""
  from bot_core.recognizer import match_template
  from bot_core.state import check_mood
  
  max_failure = get_max_failure()
  safe_trainings = {
    stat: data for stat, data in results.items()
    if int(data["failure"]) <= max_failure
  }
  
  if not safe_trainings:
    print("\n[INFO] No safe training found for point-based mode.")
    return None
  
  training_points = {}
  
  for stat, data in safe_trainings.items():
    points = calculate_training_points(stat, data)
    training_points[stat] = points
  
  # Find best training
  if not training_points:
    print("\n[INFO] No valid training points calculated.")
    return None
  
  best_stat = max(training_points.items(), key=lambda x: x[1])
  best_key, best_points = best_stat
  
  print(f"\n[INFO] Best training: {best_key.upper()} with {best_points:.1f} points")
  
  # Check if we should do recreation instead
  if should_do_recreation(best_points):
    return "recreation"
  
  return best_key

def calculate_training_points(stat, data):
  """Calculate points for a specific training"""
  from bot_core.recognizer import match_template
  
  # Validate input data structure
  if not isinstance(data, dict):
    print(f"[ERROR] Invalid data structure for {stat}: {type(data)}")
    return 0.0
  
  if "total_support" not in data or "support" not in data:
    print(f"[ERROR] Missing required keys in data for {stat}: {data.keys()}")
    return 0.0
  
  points = 0.0
  support_details = []
  
  # Base points: 1 point per regular supporter
  try:
    regular_supporters = int(data["total_support"])
    points += regular_supporters
    support_details.append(f"{regular_supporters} regular supporters")
  except (ValueError, TypeError) as e:
    print(f"[ERROR] Invalid total_support for {stat}: {data['total_support']} - {e}")
    return 0.0
  
  # Add special supporter bonuses
  points += calculate_special_supporter_bonuses(support_details)
  
  # Speed and Wit training bonus (+0.5 points)
  if stat.lower() in ["spd", "wit"]:
    points += 0.5
    support_details.append("Main stat bonus (+0.5)")
  
  # Rainbow supporter bonus - use real data structure
  points += calculate_rainbow_bonuses_real(stat, data, support_details)
  
  print(f"[INFO] {stat.upper()}: {points:.1f} points ({', '.join(support_details)})")
  return points

def calculate_special_supporter_bonuses(support_details):
  """Calculate bonuses from special supporters"""
  from bot_core.recognizer import match_template
  
  bonus_points = 0.0
  
  try:
    # Kitasan Black (1.5 points)
    kitasan_matches = match_template("game_assets/icons/kitasan.png", threshold=0.8)
    if kitasan_matches:
      kitasan_count = len(kitasan_matches)
      bonus_points += kitasan_count * 0.5  # 1.5 - 1.0 base = 0.5 extra
      support_details.append(f"{kitasan_count} Kitasan (+{kitasan_count * 0.5})")
    
    # Exclamation mark supporters (1.5 points)
    exclamation_matches = match_template("game_assets/icons/exclamation_mark.png", threshold=0.8)
    if exclamation_matches:
      exclamation_count = len(exclamation_matches)
      bonus_points += exclamation_count * 0.5  # 1.5 - 1.0 base = 0.5 extra
      support_details.append(f"{exclamation_count} Exclamation supporters (+{exclamation_count * 0.5})")
    
    # Director (0.5 points instead of 1.0)
    director_matches = match_template("game_assets/icons/director.png", threshold=0.8)
    if director_matches:
      director_count = len(director_matches)
      bonus_points -= director_count * 0.5  # 0.5 - 1.0 base = -0.5
      support_details.append(f"{director_count} Director (-{director_count * 0.5})")
    
    # Otonashi (0.5 points instead of 1.0)
    otonashi_matches = match_template("game_assets/icons/otonashi.png", threshold=0.8)
    if otonashi_matches:
      otonashi_count = len(otonashi_matches)
      bonus_points -= otonashi_count * 0.5  # 0.5 - 1.0 base = -0.5
      support_details.append(f"{otonashi_count} Otonashi (-{otonashi_count * 0.5})")
      
  except Exception as e:
    print(f"[WARNING] Error detecting special supporters: {e}")
  
  return bonus_points

def calculate_rainbow_bonuses_real(stat, data, support_details):
  """Calculate rainbow supporter bonuses using real bot data structure"""
  bonus_points = 0.0
  
  try:
    # Get support counts from real data structure
    # data["support"] = {"spd": 2, "sta": 1, "pwr": 0, "guts": 1, "wit": 0, "friend": 0}
    support_counts = data.get("support", {})
    
    if not isinstance(support_counts, dict):
      print(f"[WARNING] Support data is not a dictionary: {type(support_counts)} - {support_counts}")
      return bonus_points
    
    # Count matching rainbow supporters for this training type
    matching_rainbow_count = support_counts.get(stat.lower(), 0)
    
    if matching_rainbow_count > 0:
      if matching_rainbow_count == 1:
        bonus_points += 2.0  # 1 rainbow supporter = +2 points
        support_details.append(f"1 rainbow {stat.upper()} (+2.0)")
      elif matching_rainbow_count >= 2:
        bonus_points += 5.0  # 2+ rainbow supporters = +5 points
        support_details.append(f"{matching_rainbow_count} rainbow {stat.upper()} (+5.0)")
    
  except Exception as e:
    print(f"[ERROR] Error calculating rainbow bonuses: {e}")
  
  return bonus_points

def calculate_rainbow_bonuses(stat, data, support_details):
  """Calculate rainbow supporter bonuses"""
  # Safety check: ensure support is a dictionary
  support_data = data.get("support", {})
  if not isinstance(support_data, dict):
    print(f"[WARNING] Support data is not a dictionary: {type(support_data)} - {support_data}")
    return 0.0
  
  rainbow_count = support_data.get(stat, 0)
  if rainbow_count > 0:
    if rainbow_count == 1:
      support_details.append("1 rainbow supporter (+1.0)")
      return 1.0  # 2.0 - 1.0 base = 1.0 extra
    elif rainbow_count >= 2:
      support_details.append(f"{rainbow_count} rainbow supporters (+4.0)")
      return 4.0  # 5.0 - 1.0 base = 4.0 extra
  return 0.0

def should_do_recreation(best_points):
  """Check if recreation should be done instead of training"""
  from bot_core.state import check_mood
  
  if best_points < 3.0:
    current_mood = check_mood()
    if current_mood != "GREAT":
      threshold_text = "moderate" if 2.5 <= best_points < 3.0 else "low"
      print(f"\n[INFO] Training points ({best_points:.1f}) are {threshold_text} and mood is {current_mood} (not GREAT). Doing recreation for 20% bonus.")
      return True
  return False

# Training logic selector
def select_training_logic(logic_type, results):
  """Select training based on chosen logic type"""
  if logic_type == "most_support":
    return most_support_card(results)
  elif logic_type == "stat_priority":
    return stat_priority_training(results)
  elif logic_type == "rainbow_only":
    return rainbow_only_training(results, state.get_rainbow_strict())
  elif logic_type == "point_based":
    return point_based_training(results)
  elif logic_type == "balanced":
    return balanced_training(results)
  else:  # auto or unknown
    # Default auto logic (year-based)
    year = check_current_year()
    if "Junior Year" in year:
      return most_support_card(results)
    else:
      result = rainbow_training(results)
      if result is None:
        print("[INFO] Falling back to most_support_card because rainbow not available.")
        return most_support_card(results)
      return result
  
# Decide training
def do_something(results, training_logic="auto"):
  current_stats = stat_state()
  print(f"Current stats: {current_stats}")
  print(f"Training logic: {training_logic}")

  filtered = filter_by_stat_caps(results, current_stats)

  if not filtered:
    print("[INFO] All stats capped or no valid training.")
    return None

  return select_training_logic(filtered, training_logic)
