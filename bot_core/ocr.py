import easyocr
from PIL import Image
import numpy as np
import re

import easyocr
import sys
import os

# Add bot_utils to path for config access
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bot_utils'))

try:
    from config_manager import should_use_gpu
    use_gpu = should_use_gpu()
    print(f"OCR initialized with GPU: {use_gpu}")
except ImportError:
    use_gpu = False
    print("OCR initialized with GPU: False (config_manager not available)")

reader = easyocr.Reader(["en"], gpu=use_gpu)

def extract_text(pil_img: Image.Image) -> str:
  img_np = np.array(pil_img)
  result = reader.readtext(img_np)
  texts = [text[1] for text in result]
  return " ".join(texts)

def extract_number(pil_img: Image.Image) -> int:
  img_np = np.array(pil_img)
  result = reader.readtext(img_np, allowlist="0123456789")
  texts = [text[1] for text in result]
  joined_text = "".join(texts)

  digits = re.sub(r"[^\d]", "", joined_text)

  if digits:
    return int(digits)
  
  return -1
