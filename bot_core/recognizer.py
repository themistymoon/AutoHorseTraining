import cv2
import numpy as np
from PIL import ImageGrab, ImageStat
from monitor_manager import monitor_manager

from bot_utils.screenshot import capture_region

def match_template(template_path, region=None, threshold=0.85):
  # Get screenshot using monitor manager
  if region:
    screen = np.array(monitor_manager.get_screenshot(region=region))
  else:
    screen = np.array(monitor_manager.get_screenshot())
  screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

  # Load template
  template = cv2.imread(template_path, cv2.IMREAD_COLOR)  # safe default
  if template.shape[2] == 4:
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
  result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
  loc = np.where(result >= threshold)

  h, w = template.shape[:2]
  boxes = [(x, y, w, h) for (x, y) in zip(*loc[::-1])]

  return deduplicate_boxes(boxes)

def multi_match_templates(templates, screen=None, threshold=0.85):
  if screen is None:
    screen = monitor_manager.get_screenshot()
  screen_bgr = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

  results = {}
  for name, path in templates.items():
    template = cv2.imread(path, cv2.IMREAD_COLOR)
    if template is None:
      results[name] = []
      continue
    if template.shape[2] == 4:
      template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)

    result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    h, w = template.shape[:2]
    boxes = [(x, y, w, h) for (x, y) in zip(*loc[::-1])]
    results[name] = boxes
  return results

def deduplicate_boxes(boxes, min_dist=5):
  filtered = []
  for x, y, w, h in boxes:
    cx, cy = x + w // 2, y + h // 2
    if all(abs(cx - (fx + fw // 2)) > min_dist or abs(cy - (fy + fh // 2)) > min_dist
        for fx, fy, fw, fh in filtered):
      filtered.append((x, y, w, h))
  return filtered

def is_btn_active(region, treshold = 150):
  try:
    # Handle both (x, y, w, h) and (left, top, right, bottom) formats
    if len(region) == 4:
      x, y, w, h = region
      # Convert numpy types to regular ints
      x, y, w, h = int(x), int(y), int(w), int(h)
      
      # Check if this looks like (x, y, width, height) format from template matching
      # Template matching typically produces small width/height values and reasonable x,y coordinates
      if w <= 200 and h <= 200 and x >= 0 and y >= 0:  # Likely width/height format
        screenshot = capture_region((x, y, x + w, y + h))
      else:  # Assume it's already in left, top, right, bottom format
        screenshot = capture_region(region)
    else:
      screenshot = capture_region(region)
      
    grayscale = screenshot.convert("L")
    stat = ImageStat.Stat(grayscale)
    avg_brightness = stat.mean[0]

    return avg_brightness > treshold
  except Exception as e:
    print(f"[ERROR] is_btn_active failed with region {region}: {e}")
    return False
