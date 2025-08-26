"""
Configuration manager for bot settings
"""
import json
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path("config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def get_mouse_settings():
    """Get mouse movement settings from config"""
    config = load_config()
    mouse_settings = config.get('mouse_settings', {})
    
    return {
        'movement_mode': mouse_settings.get('movement_mode', 'smooth'),
        'movement_duration': mouse_settings.get('movement_duration', 0.175)
    }

def get_performance_settings():
    """Get performance settings from config"""
    config = load_config()
    performance_settings = config.get('performance_settings', {})
    
    return {
        'gpu_mode': performance_settings.get('gpu_mode', 'auto')
    }

def should_use_teleport():
    """Check if teleport mode should be used"""
    mouse_settings = get_mouse_settings()
    return mouse_settings['movement_mode'] == 'teleport'

def get_movement_duration():
    """Get movement duration for smooth mode"""
    mouse_settings = get_mouse_settings()
    return mouse_settings['movement_duration']

def should_use_gpu():
    """Determine if GPU should be used for OCR based on settings"""
    performance_settings = get_performance_settings()
    gpu_mode = performance_settings['gpu_mode']
    
    if gpu_mode == 'gpu':
        return True
    elif gpu_mode == 'cpu':
        return False
    else:  # auto mode
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
