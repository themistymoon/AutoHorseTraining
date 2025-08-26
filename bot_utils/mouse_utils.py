"""
Mouse movement utilities with configurable behavior and human-like patterns
"""
import pyautogui
import sys
import os
import time
import random
import math

# Add bot_utils to path for config access
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bot_utils'))

try:
    from config_manager import should_use_teleport, get_movement_duration
    from human_behavior import human_behavior
    
    def smart_move_and_click(x, y, clicks=1, button='left'):
        """Move mouse and click with configurable movement mode and human behavior"""
        # Add small random offset for more natural clicking
        offset_x, offset_y = human_behavior.get_click_offset()
        target_x, target_y = x + offset_x, y + offset_y
        
        if should_use_teleport():
            # Even in teleport mode, add some human-like delay
            pre_click_delay = random.uniform(0.02, 0.08)
            time.sleep(pre_click_delay)
            pyautogui.click(target_x, target_y, clicks=clicks, button=button)
        else:
            # Human-like movement with curve and natural timing
            current_pos = pyautogui.position()
            distance = math.sqrt((target_x - current_pos.x)**2 + (target_y - current_pos.y)**2)
            
            # Get human-like duration based on distance
            duration = human_behavior.get_human_mouse_duration(distance)
            
            # Move with slight curve instead of straight line
            if distance > 50:  # Only add curve for longer movements
                points = human_behavior.get_curved_mouse_points(
                    current_pos.x, current_pos.y, target_x, target_y
                )
                
                # Move through curve points
                total_time = duration
                point_duration = total_time / len(points)
                
                for point_x, point_y in points[:-1]:  # Skip last point
                    pyautogui.moveTo(point_x, point_y, duration=point_duration)
                
                # Final move to exact target
                pyautogui.moveTo(target_x, target_y, duration=point_duration)
            else:
                # Short movements - just move directly with human timing
                pyautogui.moveTo(target_x, target_y, duration=duration)
            
            # Small delay before click (human reaction time)
            click_delay = random.uniform(0.05, 0.15)
            time.sleep(click_delay)
            pyautogui.click(clicks=clicks, button=button)
    
    def smart_move_to(x, y):
        """Move mouse to position with configurable movement mode and human behavior"""
        # Add small random offset
        offset_x, offset_y = human_behavior.get_click_offset()
        target_x, target_y = x + offset_x, y + offset_y
        
        if should_use_teleport():
            # Instant teleport with tiny delay to seem more natural
            delay = random.uniform(0.01, 0.03)
            time.sleep(delay)
            pyautogui.moveTo(target_x, target_y, duration=0)
        else:
            # Human-like movement
            current_pos = pyautogui.position()
            distance = math.sqrt((target_x - current_pos.x)**2 + (target_y - current_pos.y)**2)
            duration = human_behavior.get_human_mouse_duration(distance)
            
            # Add curve for longer movements
            if distance > 50:
                points = human_behavior.get_curved_mouse_points(
                    current_pos.x, current_pos.y, target_x, target_y
                )
                
                total_time = duration
                point_duration = total_time / len(points)
                
                for point_x, point_y in points:
                    pyautogui.moveTo(point_x, point_y, duration=point_duration)
            else:
                pyautogui.moveTo(target_x, target_y, duration=duration)
            
except ImportError:
    print("Warning: config_manager or human_behavior not available, using default mouse behavior")
    
    def smart_move_and_click(x, y, clicks=1, button='left'):
        """Fallback mouse movement with default smooth behavior"""
        pyautogui.moveTo(x, y, duration=0.175)
        pyautogui.click(clicks=clicks, button=button)
    
    def smart_move_to(x, y):
        """Fallback mouse movement with default smooth behavior"""
        pyautogui.moveTo(x, y, duration=0.175)
