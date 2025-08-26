from PIL import Image, ImageEnhance
import mss
import numpy as np

def enhanced_screenshot(region=(0, 0, 1920, 1080)) -> Image.Image:
  # Import here to avoid circular imports
  from monitor_manager import monitor_manager
  
  # Get screenshot from selected monitor first
  screen = monitor_manager.get_screenshot()
  
  # Extract the specific region from the monitor screenshot
  if len(region) == 4:
    left, top, right, bottom = region
    # Ensure coordinates are within screen bounds
    left = max(0, left)
    top = max(0, top)
    right = min(screen.width, right)
    bottom = min(screen.height, bottom)
    
    pil_img = screen.crop((left, top, right, bottom))
  else:
    pil_img = screen

  pil_img = pil_img.resize((pil_img.width * 2, pil_img.height * 2), Image.BICUBIC)
  pil_img = pil_img.convert("L")
  pil_img = ImageEnhance.Contrast(pil_img).enhance(1.5)

  return pil_img

def capture_region(region=(0, 0, 1920, 1080)) -> Image.Image:
  # Import here to avoid circular imports
  from monitor_manager import monitor_manager
  
  # Get screenshot from selected monitor first
  screen = monitor_manager.get_screenshot()
  
  # Extract the specific region from the monitor screenshot
  if len(region) == 4:
    left, top, right, bottom = region
    # Ensure coordinates are within screen bounds
    left = max(0, left)
    top = max(0, top)
    right = min(screen.width, right)
    bottom = min(screen.height, bottom)
    
    return screen.crop((left, top, right, bottom))
  else:
    return screen
