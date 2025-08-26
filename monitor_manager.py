"""
Monitor Management for Overlay GUI
Provides monitor detection and configuration functionality
"""

import mss
import json
import os
from PIL import Image, ImageGrab
from pathlib import Path

class MonitorManager:
    def __init__(self, config_path="config.json"):
        self.config_path = Path(config_path)
        self.monitors = []
        self.selected_monitor = None
        self.detect_monitors()
        self.load_config()
    
    def detect_monitors(self):
        """Detect all available monitors"""
        self.monitors = []
        
        try:
            # Add full desktop option
            full_screen = ImageGrab.grab()
            self.monitors.append({
                'id': 'full_desktop',
                'name': 'Full Desktop',
                'bbox': (0, 0, full_screen.width, full_screen.height),
                'size': f"{full_screen.width}x{full_screen.height}",
                'info': 'All monitors combined'
            })
            
            # Get individual monitors from MSS
            with mss.mss() as sct:
                for i, monitor in enumerate(sct.monitors):
                    if i == 0:  # Skip monitor 0 (it's usually the full desktop)
                        continue
                    
                    left = monitor['left']
                    top = monitor['top']
                    width = monitor['width']
                    height = monitor['height']
                    right = left + width
                    bottom = top + height
                    
                    self.monitors.append({
                        'id': f'monitor_{i}',
                        'name': f'Monitor {i}',
                        'bbox': (left, top, right, bottom),
                        'size': f"{width}x{height}",
                        'info': f"Position: ({left}, {top}) Size: {width}x{height}"
                    })
            
            # If no individual monitors found, create estimated options
            if len(self.monitors) == 1:  # Only full desktop
                self.add_estimated_monitors(full_screen)
                
        except Exception as e:
            print(f"[ERROR] Monitor detection failed: {e}")
            # Fallback to basic setup
            self.monitors = [{
                'id': 'fallback',
                'name': 'Default Monitor',
                'bbox': (0, 0, 1920, 1080),
                'size': '1920x1080',
                'info': 'Fallback monitor'
            }]
    
    def add_estimated_monitors(self, full_screen):
        """Add estimated monitor configurations"""
        full_width = full_screen.width
        full_height = full_screen.height
        
        # Check for side-by-side dual monitors
        if full_width > 1920:
            half_width = full_width // 2
            self.monitors.extend([
                {
                    'id': 'estimated_left',
                    'name': 'Left Monitor (Est.)',
                    'bbox': (0, 0, half_width, full_height),
                    'size': f"{half_width}x{full_height}",
                    'info': 'Estimated left monitor'
                },
                {
                    'id': 'estimated_right',
                    'name': 'Right Monitor (Est.)',
                    'bbox': (half_width, 0, full_width, full_height),
                    'size': f"{half_width}x{full_height}",
                    'info': 'Estimated right monitor'
                }
            ])
        
        # Check for vertically stacked monitors
        if full_height > 1080:
            half_height = full_height // 2
            self.monitors.extend([
                {
                    'id': 'estimated_top',
                    'name': 'Top Monitor (Est.)',
                    'bbox': (0, 0, full_width, half_height),
                    'size': f"{full_width}x{half_height}",
                    'info': 'Estimated top monitor'
                },
                {
                    'id': 'estimated_bottom',
                    'name': 'Bottom Monitor (Est.)',
                    'bbox': (0, half_height, full_width, full_height),
                    'size': f"{full_width}x{half_height}",
                    'info': 'Estimated bottom monitor'
                }
            ])
    
    def get_monitors(self):
        """Get list of all detected monitors"""
        return self.monitors
    
    def get_monitor_by_id(self, monitor_id):
        """Get monitor info by ID"""
        for monitor in self.monitors:
            if monitor['id'] == monitor_id:
                return monitor
        return None
    
    def set_selected_monitor(self, monitor_id):
        """Set the selected monitor"""
        monitor = self.get_monitor_by_id(monitor_id)
        if monitor:
            self.selected_monitor = monitor
            self.save_config()
            return True
        return False
    
    def get_selected_monitor(self):
        """Get currently selected monitor"""
        return self.selected_monitor
    
    def get_screenshot(self, region=None):
        """Get screenshot from selected monitor"""
        try:
            if self.selected_monitor:
                bbox = self.selected_monitor['bbox']
                
                # Use MSS for more reliable capture
                monitor_dict = {
                    "left": bbox[0],
                    "top": bbox[1], 
                    "width": bbox[2] - bbox[0],
                    "height": bbox[3] - bbox[1]
                }
                
                with mss.mss() as sct:
                    screenshot = sct.grab(monitor_dict)
                    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                
                # Apply region cropping if specified
                # NOTE: Region coordinates should be relative to the monitor, not absolute desktop coordinates
                if region:
                    left, top, right, bottom = region
                    
                    # Ensure coordinates are within the monitor's bounds (not desktop bounds)
                    left = max(0, left)
                    top = max(0, top)
                    right = min(img.width, right)
                    bottom = min(img.height, bottom)
                    
                    # Additional safety check
                    if right <= left or bottom <= top:
                        print(f"[WARNING] Invalid region coordinates: ({left}, {top}, {right}, {bottom})")
                        print(f"[WARNING] Monitor size: {img.width}x{img.height}")
                        print(f"[WARNING] Original region: {region}")
                        return img  # Return full image if region is invalid
                    
                    img = img.crop((left, top, right, bottom))
                
                return img
            else:
                # Fallback to default ImageGrab
                return ImageGrab.grab(bbox=region)
                
        except Exception as e:
            print(f"[ERROR] Screenshot failed: {e}")
            print(f"[ERROR] Monitor: {self.selected_monitor['name'] if self.selected_monitor else 'None'}")
            print(f"[ERROR] Region: {region}")
            return ImageGrab.grab(bbox=region)
    
    def monitor_to_screen_coords(self, x, y):
        """Convert monitor-relative coordinates to absolute screen coordinates"""
        if self.selected_monitor:
            bbox = self.selected_monitor['bbox']
            # Add monitor's offset to relative coordinates
            abs_x = bbox[0] + x
            abs_y = bbox[1] + y
            return abs_x, abs_y
        else:
            # No monitor selected, assume coordinates are already absolute
            return x, y
    
    def test_monitor_ocr(self, monitor_id):
        """Test OCR on a specific monitor"""
        try:
            # Temporarily set monitor for testing
            old_monitor = self.selected_monitor
            if not self.set_selected_monitor(monitor_id):
                return None
            
            # Take screenshot
            screenshot = self.get_screenshot()
            
            # Test OCR on top portion
            test_region = screenshot.crop((0, 0, min(500, screenshot.width), min(300, screenshot.height)))
            
            # Import and run OCR
            from bot_core.ocr import extract_text
            extracted_text = extract_text(test_region)
            
            # Restore old monitor
            self.selected_monitor = old_monitor
            
            return extracted_text
            
        except Exception as e:
            print(f"[ERROR] OCR test failed: {e}")
            return None
    
    def save_config(self):
        """Save monitor configuration to config file"""
        try:
            # Load existing config
            config = {}
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            
            # Add monitor configuration
            if self.selected_monitor:
                config['monitor_config'] = {
                    'selected_monitor_id': self.selected_monitor['id'],
                    'selected_monitor_name': self.selected_monitor['name'],
                    'bbox': self.selected_monitor['bbox'],
                    'size': self.selected_monitor['size']
                }
            
            # Save config
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            print(f"[INFO] Monitor config saved: {self.selected_monitor['name']}")
            
        except Exception as e:
            print(f"[ERROR] Could not save monitor config: {e}")
    
    def load_config(self):
        """Load monitor configuration from config file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                
                if 'monitor_config' in config:
                    monitor_id = config['monitor_config'].get('selected_monitor_id')
                    if monitor_id:
                        self.set_selected_monitor(monitor_id)
                        print(f"[INFO] Loaded monitor config: {self.selected_monitor['name']}")
                        return
            
            # No config found, default to first monitor
            if self.monitors:
                self.selected_monitor = self.monitors[0]
                print(f"[INFO] Using default monitor: {self.selected_monitor['name']}")
                
        except Exception as e:
            print(f"[ERROR] Could not load monitor config: {e}")
            if self.monitors:
                self.selected_monitor = self.monitors[0]

# Global monitor manager instance
monitor_manager = MonitorManager()
