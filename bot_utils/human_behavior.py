"""
Human-like behavior module for anti-detection
"""
import random
import time
import math

class HumanBehavior:
    def __init__(self):
        self.last_action_time = time.time()
        self.action_count = 0
        self.session_start = time.time()
        
    def get_human_delay(self, base_delay=0.5, variation=0.3):
        """Get human-like delay with natural variation"""
        # Add fatigue effect - longer delays as session progresses
        session_time = time.time() - self.session_start
        fatigue_factor = min(1.2, 1.0 + (session_time / 3600) * 0.2)  # 20% slower after 1 hour
        
        # Random variation using normal distribution
        delay = random.normalvariate(base_delay, variation)
        delay = max(0.1, delay * fatigue_factor)  # Minimum 0.1 second
        
        return delay
    
    def get_human_mouse_duration(self, distance=100, base_duration=0.3):
        """Get human-like mouse movement duration based on distance"""
        # Fitts's Law inspired timing
        log_factor = math.log2(max(distance / 10, 2))  # Avoid log(0)
        duration = base_duration * log_factor
        
        # Add randomization
        variation = random.uniform(0.8, 1.3)
        duration *= variation
        
        return max(0.05, min(2.0, duration))  # Clamp between 0.05 and 2 seconds
    
    def get_click_offset(self, max_offset=3):
        """Get small random offset for more human-like clicking"""
        x_offset = random.uniform(-max_offset, max_offset)
        y_offset = random.uniform(-max_offset, max_offset)
        return int(x_offset), int(y_offset)
    
    def should_take_break(self):
        """Determine if bot should take a natural break"""
        # Take break every 15-45 minutes
        session_time = time.time() - self.session_start
        break_interval = random.uniform(900, 2700)  # 15-45 minutes
        
        if session_time > break_interval:
            self.session_start = time.time()  # Reset timer
            return True, random.uniform(30, 180)  # 30 seconds to 3 minutes break
        
        return False, 0
    
    def add_thinking_delay(self):
        """Add human-like thinking/reaction time"""
        # Simulate reading screen and deciding what to do
        thinking_time = random.normalvariate(1.2, 0.4)  # Average 1.2s thinking
        thinking_time = max(0.3, min(3.0, thinking_time))  # Clamp 0.3-3s
        
        time.sleep(thinking_time)
    
    def add_micro_break(self):
        """Add small random pauses"""
        if random.random() < 0.1:  # 10% chance
            micro_break = random.uniform(0.5, 2.0)
            time.sleep(micro_break)
    
    def get_curved_mouse_points(self, start_x, start_y, end_x, end_y, num_points=5):
        """Generate curved mouse movement points instead of straight line"""
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            
            # Add some curve using bezier-like calculation
            mid_x = (start_x + end_x) / 2 + random.uniform(-20, 20)
            mid_y = (start_y + end_y) / 2 + random.uniform(-20, 20)
            
            # Quadratic interpolation for curve
            x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
            
            points.append((int(x), int(y)))
        
        return points
    
    def should_make_mistake(self):
        """Occasionally make human-like mistakes"""
        # 2% chance to make a small mistake (like slight misclick)
        return random.random() < 0.02
    
    def get_reading_delay(self, text_length=50):
        """Get time needed to 'read' text like a human"""
        # Average reading speed: 200-250 words per minute
        words = text_length / 5  # Approximate words
        reading_time = (words / 225) * 60  # 225 wpm average
        
        # Add some variation
        reading_time *= random.uniform(0.7, 1.4)
        
        return max(0.5, reading_time)

# Global instance
human_behavior = HumanBehavior()
