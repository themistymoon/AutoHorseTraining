import tkinter as tk
from tkinter import ttk
import json
import os
import threading
import time
import sys
import traceback

# Add paths for bot functionality
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot_core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'bot_utils'))

# Import bot functionality
try:
    import bot_core.state as state
    from bot_core.execute import career_lobby_iteration
    from bot_utils.screenshot import capture_region, enhanced_screenshot
    # Import OCR separately to handle potential issues
    try:
        from bot_core.ocr import extract_text
        OCR_AVAILABLE = True
    except ImportError:
        OCR_AVAILABLE = False
        print("OCR functionality not available")
    import pygetwindow as gw
    from hotkey_manager import start_global_hotkeys, stop_global_hotkeys
    BOT_AVAILABLE = True
except ImportError as e:
    print(f"Bot functionality not available: {e}")
    BOT_AVAILABLE = False
    OCR_AVAILABLE = False

class TrainingAssistant:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_colors()
        self.setup_styles()
        self.create_interface()
        self.setup_draggable()
        self.initialize_data()
        
        # Bot control state
        self.bot_thread = None
        self.bot_running = False
        self.current_hotkey = "f1"  # Default hotkey
        
        # Start F1 hotkey listener
        if BOT_AVAILABLE:
            try:
                from hotkey_manager import HotkeyManager
                global hotkey_manager
                hotkey_manager = HotkeyManager(self)
                hotkey_manager.current_hotkey = self.current_hotkey
                hotkey_manager.start_hotkey_listener()
                print(f"✅ {self.current_hotkey.upper()} hotkey listener started")
            except Exception as e:
                print(f"⚠️ Hotkey failed to start: {e}")
        
    def setup_window(self):
        """Setup the overlay window properties"""
        self.root.title("🎯 Training Assistant")
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.94)
        self.root.overrideredirect(True)
        
        # Set window size and position
        window_width = 380
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - window_width - 20
        y = 50
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
    def setup_colors(self):
        """Setup dark theme colors"""
        self.colors = {
            'bg': '#1e1e1e',
            'accent': '#0078d4',
            'success': '#107c10',
            'warning': '#ff8c00',
            'danger': '#d13438',
            'text': '#ffffff',
            'text_secondary': '#cccccc',
            'border': '#404040'
        }
        self.root.configure(bg=self.colors['bg'])
        
    def setup_styles(self):
        """Setup modern dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame styles
        style.configure('Dark.TFrame', background=self.colors['bg'], relief='flat')
        style.configure('Title.TFrame', background=self.colors['accent'], relief='flat')
        
        # Label styles
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['text'], font=('Segoe UI', 9))
        style.configure('Title.TLabel', background=self.colors['bg'], foreground=self.colors['text'], font=('Segoe UI', 12, 'bold'))
        style.configure('Header.TLabel', background=self.colors['accent'], foreground='white', font=('Segoe UI', 11, 'bold'))
        style.configure('Status.TLabel', background=self.colors['bg'], foreground=self.colors['text_secondary'], font=('Segoe UI', 10))
        
        # Button styles
        style.configure('Modern.TButton', background=self.colors['accent'], foreground='white', borderwidth=0, 
                       focuscolor='none', font=('Segoe UI', 9))
        style.configure('Success.TButton', background=self.colors['success'], foreground='white', borderwidth=0)
        style.configure('Danger.TButton', background=self.colors['danger'], foreground='white', borderwidth=0)
        
        # Checkbutton style
        style.configure('Dark.TCheckbutton', background=self.colors['bg'], foreground=self.colors['text'], focuscolor='none')
        
    def create_interface(self):
        """Create the main interface"""
        # Title bar
        self.title_frame = ttk.Frame(self.root, style='Title.TFrame', height=40)
        self.title_frame.pack(fill=tk.X)
        self.title_frame.pack_propagate(False)
        
        title_label = ttk.Label(self.title_frame, text="🎯 Training Assistant", style='Header.TLabel')
        title_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        # Close button
        close_btn = ttk.Button(self.title_frame, text="✕", width=3, command=self.close_application, style='Danger.TButton')
        close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Minimize button
        minimize_btn = ttk.Button(self.title_frame, text="─", width=3, command=self.minimize_window, style='Modern.TButton')
        minimize_btn.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
        
        # Main content with scrolling
        self.create_scrollable_content()
        
        # Resize handle
        resize_frame = ttk.Frame(self.root, style='Dark.TFrame', height=20)
        resize_frame.pack(side=tk.BOTTOM, fill=tk.X)
        resize_label = ttk.Label(resize_frame, text="⋮⋮⋮", style='Dark.TLabel', anchor=tk.CENTER)
        resize_label.pack(expand=True)
        
    def create_scrollable_content(self):
        """Create scrollable content area"""
        # Container for canvas and scrollbar
        scroll_container = ttk.Frame(self.root, style='Dark.TFrame')
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(scroll_container, bg=self.colors['bg'], highlightthickness=0)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scrollable frame
        self.content_frame = ttk.Frame(self.canvas, style='Dark.TFrame')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel to canvas and content
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.content_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Make canvas focusable and bind focus events
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", lambda e: self.canvas.focus_set())
        
        # Configure scrolling
        def configure_scroll(event):
            # Update scroll region with a small delay to ensure proper calculation
            self.root.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        self.content_frame.bind("<Configure>", configure_scroll)
        self.canvas.bind("<Configure>", configure_scroll)
        
        # Create all content sections
        self.create_all_content()
        
    def create_all_content(self):
        """Create all content sections in one beautiful layout"""
        # Status Section
        self.create_section_header("🤖 Status")
        status_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        status_row.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(status_row, text="Bot:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_row, text="● STOPPED", foreground=self.colors['danger'], style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(8, 20))
        
        ttk.Label(status_row, text="Skills:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.skill_status_label = ttk.Label(status_row, text="Not Active", foreground=self.colors['text_secondary'], style='Status.TLabel')
        self.skill_status_label.pack(side=tk.LEFT, padx=(8, 0))
        
        # Controls Section (moved to be right after Status)
        self.create_section_header("🎮 Controls")
        
        # Main control row with start button and hotkey button
        control_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        control_row.pack(fill=tk.X, pady=(0, 5))
        
        self.start_button = ttk.Button(control_row, text="▶️ Start Training", command=self.toggle_bot, style='Success.TButton')
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        
        self.hotkey_button = ttk.Button(control_row, text="⌨️ F1", command=self.edit_hotkey, style='Modern.TButton')
        self.hotkey_button.pack(side=tk.RIGHT, padx=(3, 0))
        
        # Quick action buttons
        action_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        action_row.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(action_row, text="📸 Test Screenshot", command=self.test_screenshot, style='Modern.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        ttk.Button(action_row, text="👁️ Test OCR", command=self.test_ocr, style='Modern.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        ttk.Button(action_row, text="📝 Skills", command=self.open_skills_editor, style='Modern.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))
        
        # Training Priority Section
        self.create_section_header("🏃 Training Priority")
        
        priority_info = ttk.Label(self.content_frame, text="Top = Highest Priority", style='Dark.TLabel', foreground=self.colors['text_secondary'])
        priority_info.pack(anchor=tk.W, pady=(0, 5))
        
        priority_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        priority_row.pack(fill=tk.X, pady=(0, 15))
        
        self.priority_listbox = tk.Listbox(priority_row, height=5, bg=self.colors['bg'], fg=self.colors['text'],
                                          selectbackground=self.colors['accent'], borderwidth=0, relief='flat', font=('Segoe UI', 9))
        self.priority_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        priority_buttons = ttk.Frame(priority_row, style='Dark.TFrame')
        priority_buttons.pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(priority_buttons, text="↑", command=self.move_priority_up, style='Modern.TButton', width=3).pack(pady=2)
        ttk.Button(priority_buttons, text="↓", command=self.move_priority_down, style='Modern.TButton', width=3).pack()
        
        # Settings Section
        self.create_section_header("⚙️ Settings")
        
        # Training Logic Selection
        logic_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        logic_row.pack(fill=tk.X, pady=3)
        ttk.Label(logic_row, text="🧠 Training Logic:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.training_logic = tk.StringVar(value="auto")
        logic_dropdown = ttk.Combobox(logic_row, textvariable=self.training_logic, width=20, state="readonly")
        logic_dropdown['values'] = (
            "auto", 
            "most_support", 
            "stat_priority", 
            "rainbow_only", 
            "point_based",
            "balanced"
        )
        logic_dropdown.pack(side=tk.RIGHT)
        # Add logic info
        logic_info = ttk.Label(self.content_frame, text="• auto: Year-based logic (most support → rainbow)\n• most_support: Always choose training with most support cards\n• stat_priority: Follow stat priority order strictly\n• rainbow_only: Only do rainbow training (support type = training type)\n• point_based: Advanced scoring with supporter recognition & mood optimization\n• balanced: Equal priority for all stats", 
                              style='Dark.TLabel', foreground=self.colors['text_secondary'], font=('Segoe UI', 8), justify=tk.LEFT)
        logic_info.pack(anchor=tk.W, pady=(0, 10))
        
        # Race settings
        race_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        race_row.pack(fill=tk.X, pady=3)
        self.prioritize_g1_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(race_row, text="🏆 Prioritize G1 Races", variable=self.prioritize_g1_var, style='Dark.TCheckbutton').pack(side=tk.LEFT)
        
        training_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        training_row.pack(fill=tk.X, pady=3)
        self.cancel_consecutive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(training_row, text="🚫 Cancel Consecutive Failures", variable=self.cancel_consecutive_var, style='Dark.TCheckbutton').pack(side=tk.LEFT)
        
        skill_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        skill_row.pack(fill=tk.X, pady=(3, 15))
        self.enable_skill_buying_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(skill_row, text="💰 Enable Skill Buying", variable=self.enable_skill_buying_var, style='Dark.TCheckbutton').pack(side=tk.LEFT)
        
        # Skills Section
        self.create_section_header("🎯 Skills to Buy")
        self.skills_listbox = tk.Listbox(self.content_frame, height=4, bg=self.colors['bg'], fg=self.colors['text'],
                                        selectbackground=self.colors['accent'], borderwidth=0, relief='flat', font=('Segoe UI', 9))
        self.skills_listbox.pack(fill=tk.X, pady=(0, 15))
        
        # Additional Advanced Settings Section
        self.create_section_header("⚙️ Advanced Settings")
        
        # Failure Chance Settings
        failure_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        failure_row.pack(fill=tk.X, pady=3)
        ttk.Label(failure_row, text="🎲 Max Failure Chance (%):", style='Dark.TLabel').pack(side=tk.LEFT)
        self.failure_chance = tk.StringVar(value="20")
        failure_entry = ttk.Entry(failure_row, textvariable=self.failure_chance, width=5)
        failure_entry.pack(side=tk.RIGHT)
        # Add validation tooltip
        failure_info = ttk.Label(failure_row, text="(0-100)", style='Dark.TLabel', foreground=self.colors['text_secondary'])
        failure_info.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Minimal Mood Settings
        mood_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        mood_row.pack(fill=tk.X, pady=3)
        ttk.Label(mood_row, text="😊 Minimal Mood Level:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.minimal_mood = tk.StringVar(value="3")
        mood_entry = ttk.Entry(mood_row, textvariable=self.minimal_mood, width=5)
        mood_entry.pack(side=tk.RIGHT)
        # Add validation tooltip
        mood_info = ttk.Label(mood_row, text="(1-5)", style='Dark.TLabel', foreground=self.colors['text_secondary'])
        mood_info.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Rainbow Strict Mode
        rainbow_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        rainbow_row.pack(fill=tk.X, pady=3)
        ttk.Label(rainbow_row, text="🌈 Rainbow Strict Mode:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.rainbow_strict = tk.BooleanVar(value=True)
        rainbow_check = ttk.Checkbutton(rainbow_row, variable=self.rainbow_strict, style='Dark.TCheckbutton')
        rainbow_check.pack(side=tk.RIGHT)
        # Add explanation tooltip
        rainbow_info = ttk.Label(rainbow_row, text="(rest if no rainbow)", style='Dark.TLabel', foreground=self.colors['text_secondary'])
        rainbow_info.pack(side=tk.RIGHT, padx=(0, 5))
        
        # OCR Settings
        ocr_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        ocr_row.pack(fill=tk.X, pady=3)
        ttk.Label(ocr_row, text="👁️ OCR Confidence (%):", style='Dark.TLabel').pack(side=tk.LEFT)
        self.ocr_confidence = tk.StringVar(value="80")
        ocr_entry = ttk.Entry(ocr_row, textvariable=self.ocr_confidence, width=5)
        ocr_entry.pack(side=tk.RIGHT)
        # Add validation tooltip
        ocr_info = ttk.Label(ocr_row, text="(50-99)", style='Dark.TLabel', foreground=self.colors['text_secondary'])
        ocr_info.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Action Delay
        delay_row = ttk.Frame(self.content_frame, style='Dark.TFrame')
        delay_row.pack(fill=tk.X, pady=3)
        ttk.Label(delay_row, text="⏱️ Action Delay (ms):", style='Dark.TLabel').pack(side=tk.LEFT)
        self.action_delay = tk.StringVar(value="500")
        delay_entry = ttk.Entry(delay_row, textvariable=self.action_delay, width=5)
        delay_entry.pack(side=tk.RIGHT)
        # Add validation tooltip
        delay_info = ttk.Label(delay_row, text="(100-5000)", style='Dark.TLabel', foreground=self.colors['text_secondary'])
        delay_info.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Debug Section
        self.create_section_header("🐛 Debug Options")
        
        debug_row1 = ttk.Frame(self.content_frame, style='Dark.TFrame')
        debug_row1.pack(fill=tk.X, pady=3)
        self.debug_logging_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(debug_row1, text="🔍 Enable Debug Logging", variable=self.debug_logging_var, style='Dark.TCheckbutton').pack(side=tk.LEFT)
        
        debug_row2 = ttk.Frame(self.content_frame, style='Dark.TFrame')
        debug_row2.pack(fill=tk.X, pady=3)
        self.save_screenshots_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(debug_row2, text="📷 Save Debug Screenshots", variable=self.save_screenshots_var, style='Dark.TCheckbutton').pack(side=tk.LEFT)
        
        # Info Section
        self.create_section_header("ℹ️ Information")
        info_text = ttk.Label(self.content_frame, text="Version: 2.0.0\nMode: Training Assistant\nStatus: Ready", 
                             style='Dark.TLabel', justify=tk.LEFT)
        info_text.pack(anchor=tk.W, pady=(0, 20))
        
    def create_section_header(self, title):
        """Create a beautiful section header"""
        header = ttk.Label(self.content_frame, text=title, style='Title.TLabel')
        header.pack(anchor=tk.W, pady=(10, 8))
        
    def setup_draggable(self):
        """Make window draggable"""
        self.title_frame.bind("<Button-1>", self.start_drag)
        self.title_frame.bind("<B1-Motion>", self.do_drag)
        
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def initialize_data(self):
        """Initialize data and load config"""
        # Initialize priority listbox
        stats = ["Speed", "Stamina", "Power", "Guts", "Wisdom"]
        for stat in stats:
            self.priority_listbox.insert(tk.END, stat)
            
        # Initialize skills listbox
        skills = ["Speed Star ⭐", "Stamina Boost 💪", "Power Drive 🔥", "Mental Strength 🧠"]
        for skill in skills:
            self.skills_listbox.insert(tk.END, skill)
            
        # Load saved settings
        self.load_settings()
    
    def load_settings(self):
        """Load settings from config file"""
        try:
            if os.path.exists("gui_config.json"):
                with open("gui_config.json", "r") as f:
                    config = json.load(f)
                    
                # Load checkbox settings
                self.prioritize_g1_var.set(config.get("prioritize_g1", True))
                self.cancel_consecutive_var.set(config.get("cancel_consecutive", False))
                self.enable_skill_buying_var.set(config.get("enable_skill_buying", False))
                self.debug_logging_var.set(config.get("debug_logging", False))
                self.save_screenshots_var.set(config.get("save_screenshots", False))
                
                # Load training logic
                self.training_logic.set(config.get("training_logic", "auto"))
                
                # Load numeric settings
                self.failure_chance.set(str(config.get("failure_chance", 20)))
                self.minimal_mood.set(str(config.get("minimal_mood", 3)))
                self.rainbow_strict.set(config.get("rainbow_strict", True))
                self.ocr_confidence.set(str(config.get("ocr_confidence", 80)))
                self.action_delay.set(str(config.get("action_delay", 500)))
                
                # Load hotkey
                self.current_hotkey = config.get("hotkey", "f1")
                self.update_hotkey_button()
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save current settings to config file"""
        try:
            config = {
                # Checkbox settings
                "prioritize_g1": self.prioritize_g1_var.get(),
                "cancel_consecutive": self.cancel_consecutive_var.get(),
                "enable_skill_buying": self.enable_skill_buying_var.get(),
                "debug_logging": self.debug_logging_var.get(),
                "save_screenshots": self.save_screenshots_var.get(),
                
                # Training logic
                "training_logic": self.training_logic.get(),
                
                # Numeric settings
                "failure_chance": int(self.failure_chance.get() or 20),
                "minimal_mood": int(self.minimal_mood.get() or 3),
                "rainbow_strict": self.rainbow_strict.get(),
                "ocr_confidence": int(self.ocr_confidence.get() or 80),
                "action_delay": int(self.action_delay.get() or 500),
                
                # Hotkey setting
                "hotkey": self.current_hotkey,
                
                # Priority order
                "priority_order": [self.priority_listbox.get(i) for i in range(self.priority_listbox.size())],
                
                # Selected skills
                "selected_skills": [self.skills_listbox.get(i) for i in range(self.skills_listbox.size())]
            }
            
            with open("gui_config.json", "w") as f:
                json.dump(config, f, indent=2)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def get_current_config(self):
        """Get current configuration for bot use"""
        try:
            return {
                "prioritize_g1": self.prioritize_g1_var.get(),
                "cancel_consecutive": self.cancel_consecutive_var.get(),
                "enable_skill_buying": self.enable_skill_buying_var.get(),
                "debug_logging": self.debug_logging_var.get(),
                "save_screenshots": self.save_screenshots_var.get(),
                "training_logic": self.training_logic.get(),
                "failure_chance": int(self.failure_chance.get() or 20),
                "minimal_mood": int(self.minimal_mood.get() or 3),
                "rainbow_strict": self.rainbow_strict.get(),
                "ocr_confidence": int(self.ocr_confidence.get() or 80),
                "action_delay": int(self.action_delay.get() or 500),
                "priority_order": [self.priority_listbox.get(i) for i in range(self.priority_listbox.size())],
                "selected_skills": [self.skills_listbox.get(i) for i in range(self.skills_listbox.size())]
            }
        except Exception as e:
            print(f"Error getting config: {e}")
            return {}
    
    def edit_hotkey(self):
        """Open hotkey editor dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⌨️ Edit Hotkey")
        dialog.geometry("300x150")
        dialog.wm_attributes("-topmost", True)
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Center on parent
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(dialog, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Info label
        info_label = ttk.Label(main_frame, text="Press any key to set as hotkey:", style='Dark.TLabel')
        info_label.pack(pady=(0, 10))
        
        # Current hotkey display
        current_label = ttk.Label(main_frame, text=f"Current: {self.current_hotkey.upper()}", 
                                 style='Title.TLabel', foreground=self.colors['accent'])
        current_label.pack(pady=(0, 10))
        
        # Instruction
        instruction_label = ttk.Label(main_frame, text="Click here and press a key:", style='Dark.TLabel')
        instruction_label.pack(pady=(0, 5))
        
        # Key capture entry
        key_var = tk.StringVar(value=self.current_hotkey)
        key_entry = ttk.Entry(main_frame, textvariable=key_var, justify=tk.CENTER)
        key_entry.pack(fill=tk.X, pady=(0, 10))
        key_entry.focus_set()
        
        def on_key_press(event):
            key = event.keysym.lower()
            if key in ['escape']:
                dialog.destroy()
                return
            key_var.set(key)
            
        key_entry.bind('<KeyPress>', on_key_press)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        btn_frame.pack(fill=tk.X)
        
        def save_hotkey():
            new_hotkey = key_var.get().lower()
            if new_hotkey and new_hotkey != self.current_hotkey:
                self.set_hotkey(new_hotkey)
            dialog.destroy()
            
        def cancel():
            dialog.destroy()
            
        ttk.Button(btn_frame, text="Save", command=save_hotkey, style='Success.TButton').pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Cancel", command=cancel, style='Modern.TButton').pack(side=tk.RIGHT)
    
    def set_hotkey(self, new_hotkey):
        """Set new hotkey and restart listener"""
        try:
            # Stop current hotkey listener
            if BOT_AVAILABLE:
                stop_global_hotkeys()
            
            # Update hotkey
            self.current_hotkey = new_hotkey
            self.update_hotkey_button()
            
            # Restart hotkey listener with new key
            if BOT_AVAILABLE:
                from hotkey_manager import HotkeyManager
                global hotkey_manager
                hotkey_manager = HotkeyManager(self)
                hotkey_manager.current_hotkey = new_hotkey
                hotkey_manager.start_hotkey_listener()
                print(f"✅ Hotkey changed to: {new_hotkey.upper()}")
            
            # Save settings
            self.save_settings()
            
        except Exception as e:
            print(f"⚠️ Error setting hotkey: {e}")
    
    def update_hotkey_button(self):
        """Update hotkey button text"""
        try:
            self.hotkey_button.config(text=f"⌨️ {self.current_hotkey.upper()}")
        except AttributeError:
            pass
            
    def move_priority_up(self):
        """Move selected priority item up"""
        try:
            selection = self.priority_listbox.curselection()
            if selection and selection[0] > 0:
                index = selection[0]
                item = self.priority_listbox.get(index)
                self.priority_listbox.delete(index)
                self.priority_listbox.insert(index - 1, item)
                self.priority_listbox.selection_set(index - 1)
        except Exception:
            pass
            
    def move_priority_down(self):
        """Move selected priority item down"""
        try:
            selection = self.priority_listbox.curselection()
            if selection and selection[0] < self.priority_listbox.size() - 1:
                index = selection[0]
                item = self.priority_listbox.get(index)
                self.priority_listbox.delete(index)
                self.priority_listbox.insert(index + 1, item)
                self.priority_listbox.selection_set(index + 1)
        except Exception:
            pass
            
    def toggle_bot(self):
        """Toggle bot start/stop"""
        if not BOT_AVAILABLE:
            self.status_label.config(text="❌ Bot not available", foreground=self.colors['danger'])
            return
            
        if not self.bot_running:
            self.start_bot()
        else:
            self.stop_bot()
            
    def start_bot(self):
        """Start the training bot"""
        try:
            # Focus Umamusume window first
            if not self.focus_umamusume():
                self.status_label.config(text="❌ Umamusume not found", foreground=self.colors['danger'])
                return
            
            # Save current settings before starting
            self.save_settings()
            
            # Apply settings to bot config if available
            if BOT_AVAILABLE and hasattr(state, 'set_gui_config'):
                config = self.get_current_config()
                state.set_gui_config(config)
                
            # Start bot thread
            self.bot_running = True
            self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
            self.bot_thread.start()
            
            # Update UI
            self.start_button.config(text="⏹️ Stop Training", style='Danger.TButton')
            self.status_label.config(text="🔄 RUNNING", foreground=self.colors['success'])
            
        except Exception as e:
            self.status_label.config(text=f"❌ Start failed: {str(e)}", foreground=self.colors['danger'])
            self.bot_running = False
            
    def stop_bot(self):
        """Stop the training bot"""
        self.bot_running = False
        if hasattr(state, 'is_bot_running'):
            state.is_bot_running = False
            
        # Update UI
        self.start_button.config(text="▶️ Start Training", style='Success.TButton')
        self.status_label.config(text="● STOPPED", foreground=self.colors['danger'])
        
    def focus_umamusume(self):
        """Focus the Umamusume window"""
        try:
            win = gw.getWindowsWithTitle("Umamusume")
            target_window = next((w for w in win if w.title.strip() == "Umamusume"), None)
            if not target_window:
                return False
                
            if target_window.isMinimized:
                target_window.restore()
            else:
                target_window.minimize()
                time.sleep(0.2)
                target_window.restore()
                time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Error focusing window: {e}")
            return False
            
    def bot_loop(self):
        """Main bot loop"""
        try:
            state.reload_config()
            state.is_bot_running = True
            
            while self.bot_running:
                try:
                    career_lobby_iteration()
                    if not self.bot_running:
                        break
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Bot iteration error: {e}")
                    break
                    
        except Exception as e:
            print(f"Bot loop error: {e}")
        finally:
            state.is_bot_running = False
            # Update UI on main thread
            self.root.after(0, self.stop_bot)
            
    def test_screenshot(self):
        """Test screenshot functionality"""
        if not BOT_AVAILABLE:
            self.status_label.config(text="❌ Screenshot not available", foreground=self.colors['danger'])
            return
            
        try:
            # Take a screenshot
            screenshot = capture_region()
            screenshot.save("test_screenshot.png")
            self.status_label.config(text="📸 Screenshot saved!", foreground=self.colors['success'])
            self.root.after(3000, lambda: self.status_label.config(text="● STOPPED", foreground=self.colors['danger']))
        except Exception as e:
            self.status_label.config(text=f"❌ Screenshot failed: {str(e)}", foreground=self.colors['danger'])
            self.root.after(3000, lambda: self.status_label.config(text="● STOPPED", foreground=self.colors['danger']))
        
    def test_ocr(self):
        """Test OCR functionality"""
        if not BOT_AVAILABLE:
            self.status_label.config(text="❌ Bot not available", foreground=self.colors['danger'])
            return
            
        if not OCR_AVAILABLE:
            self.status_label.config(text="❌ OCR not available", foreground=self.colors['danger'])
            return
            
        try:
            # Take a screenshot and run OCR
            self.status_label.config(text="🔄 Running OCR...", foreground=self.colors['accent'])
            
            def run_ocr():
                try:
                    screenshot = enhanced_screenshot()
                    text = extract_text(screenshot)
                    print(f"OCR Result: {text}")
                    
                    # Update UI on main thread
                    self.root.after(0, lambda: self.status_label.config(text="👁️ OCR complete!", foreground=self.colors['success']))
                    self.root.after(3000, lambda: self.status_label.config(text="● STOPPED", foreground=self.colors['danger']))
                except Exception as e:
                    print(f"OCR Error: {e}")
                    self.root.after(0, lambda: self.status_label.config(text=f"❌ OCR failed: {str(e)}", foreground=self.colors['danger']))
                    self.root.after(3000, lambda: self.status_label.config(text="● STOPPED", foreground=self.colors['danger']))
            
            # Run OCR in separate thread to avoid blocking UI
            threading.Thread(target=run_ocr, daemon=True).start()
            
        except Exception as e:
            self.status_label.config(text=f"❌ OCR failed: {str(e)}", foreground=self.colors['danger'])
            self.root.after(3000, lambda: self.status_label.config(text="● STOPPED", foreground=self.colors['danger']))
        
    def open_skills_editor(self):
        """Open skills editor window"""
        try:
            # Create skills editor window
            skills_window = tk.Toplevel(self.root)
            skills_window.title("🎯 Skills Editor")
            skills_window.geometry("450x600")
            skills_window.configure(bg=self.colors['bg'])
            skills_window.resizable(True, True)
            
            # Make it stay on top and modal
            skills_window.transient(self.root)
            skills_window.grab_set()
            
            # Title bar
            title_frame = ttk.Frame(skills_window, style='Title.TFrame', height=40)
            title_frame.pack(fill=tk.X)
            title_frame.pack_propagate(False)
            
            title_label = ttk.Label(title_frame, text="🎯 Skills Editor", style='Header.TLabel')
            title_label.pack(side=tk.LEFT, padx=10, pady=8)
            
            close_btn = ttk.Button(title_frame, text="✕", width=3, command=skills_window.destroy, style='Danger.TButton')
            close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
            
            # Main content frame
            main_frame = ttk.Frame(skills_window, style='Dark.TFrame')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Instructions
            instructions = ttk.Label(main_frame, text="Select skills to include in auto-buying:", 
                                   style='Dark.TLabel', font=('Segoe UI', 10))
            instructions.pack(anchor=tk.W, pady=(0, 10))
            
            # Skills frame with scrollbar
            skills_frame = ttk.Frame(main_frame, style='Dark.TFrame')
            skills_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Create canvas for scrollable skills list
            canvas = tk.Canvas(skills_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(skills_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Sample skills with categories
            skills_data = {
                "🏃 Speed Skills": [
                    "Speed Star ⭐", "Quick Acceleration 🚀", "Top Speed Master 💨",
                    "Sprint Specialist ⚡", "Pace Maker 🎯"
                ],
                "💪 Stamina Skills": [
                    "Endurance Beast 💪", "Distance Runner 🏃", "Stamina Boost 🔋",
                    "Long Distance Pro 🛤️", "Recovery Master 💚"
                ],
                "🔥 Power Skills": [
                    "Power Drive 🔥", "Explosive Force 💥", "Strength Builder 🏋️",
                    "Power Surge ⚡", "Heavy Impact 💨"
                ],
                "🥊 Guts Skills": [
                    "Mental Strength 🧠", "Never Give Up 🥊", "Fighting Spirit 👊",
                    "Determination 💎", "Pressure Resistant 🛡️"
                ],
                "🧠 Wisdom Skills": [
                    "Strategic Mind 🧠", "Quick Learner 📚", "Skill Master 🎓",
                    "Tactical Genius ♟️", "Race Intelligence 💡"
                ]
            }
            
            # Store skill checkboxes
            self.skill_checkboxes = {}
            
            # Create skill checkboxes by category
            for category, skills in skills_data.items():
                # Category header
                category_label = ttk.Label(scrollable_frame, text=category, 
                                         style='Title.TLabel', font=('Segoe UI', 11, 'bold'))
                category_label.pack(anchor=tk.W, pady=(10, 5))
                
                # Skills in this category
                for skill in skills:
                    skill_var = tk.BooleanVar()
                    # Check if skill is already in the main skills listbox
                    if any(skill in self.skills_listbox.get(i) for i in range(self.skills_listbox.size())):
                        skill_var.set(True)
                    
                    checkbox = ttk.Checkbutton(scrollable_frame, text=skill, 
                                             variable=skill_var, style='Dark.TCheckbutton')
                    checkbox.pack(anchor=tk.W, padx=20, pady=2)
                    self.skill_checkboxes[skill] = skill_var
            
            # Buttons frame
            btn_frame = ttk.Frame(main_frame, style='Dark.TFrame')
            btn_frame.pack(fill=tk.X, pady=(10, 0))
            
            # Select All / Deselect All buttons
            select_frame = ttk.Frame(btn_frame, style='Dark.TFrame')
            select_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Button(select_frame, text="✅ Select All", command=lambda: self.toggle_all_skills(True),
                      style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(select_frame, text="❌ Deselect All", command=lambda: self.toggle_all_skills(False),
                      style='Modern.TButton').pack(side=tk.LEFT)
            
            # Apply and Cancel buttons
            action_frame = ttk.Frame(btn_frame, style='Dark.TFrame')
            action_frame.pack(fill=tk.X)
            
            ttk.Button(action_frame, text="💾 Apply Changes", command=lambda: self.apply_skills_changes(skills_window),
                      style='Success.TButton').pack(side=tk.RIGHT, padx=(5, 0))
            ttk.Button(action_frame, text="🚫 Cancel", command=skills_window.destroy,
                      style='Danger.TButton').pack(side=tk.RIGHT)
            
            # Center the window
            skills_window.update_idletasks()
            x = (skills_window.winfo_screenwidth() // 2) - (450 // 2)
            y = (skills_window.winfo_screenheight() // 2) - (600 // 2)
            skills_window.geometry(f"450x600+{x}+{y}")
            
        except Exception as e:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", f"Failed to open skills editor: {str(e)}")
    
    def toggle_all_skills(self, select_all):
        """Toggle all skill checkboxes"""
        for skill_var in self.skill_checkboxes.values():
            skill_var.set(select_all)
    
    def apply_skills_changes(self, window):
        """Apply skills changes to the main skills listbox"""
        try:
            # Clear current skills listbox
            self.skills_listbox.delete(0, tk.END)
            
            # Add selected skills
            for skill, var in self.skill_checkboxes.items():
                if var.get():
                    self.skills_listbox.insert(tk.END, skill)
            
            # Close the window
            window.destroy()
            
            # Update status
            self.skill_status_label.config(text=f"{self.skills_listbox.size()} skills selected", 
                                         foreground=self.colors['success'])
            self.root.after(3000, lambda: self.skill_status_label.config(text="Not Active", 
                                                                        foreground=self.colors['text_secondary']))
            
        except Exception as e:
            import tkinter.messagebox as msgbox
            msgbox.showerror("Error", f"Failed to apply changes: {str(e)}")
        
    def minimize_window(self):
        """Minimize window"""
        self.root.withdraw()
        
        # Create restore window
        self.restore_window = tk.Toplevel()
        self.restore_window.title("Training Assistant (Minimized)")
        self.restore_window.geometry("200x50")
        self.restore_window.resizable(False, False)
        
        restore_btn = ttk.Button(self.restore_window, text="🔄 Restore", command=self.restore_window_func, style='Success.TButton')
        restore_btn.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def restore_window_func(self):
        """Restore window from minimize"""
        self.restore_window.destroy()
        self.root.deiconify()
        
    def close_application(self):
        """Close application with cleanup"""
        try:
            # Stop F1 hotkey listener
            if BOT_AVAILABLE:
                try:
                    stop_global_hotkeys()
                    print("🔇 F1 hotkey listener stopped")
                except Exception as e:
                    print(f"⚠️ Error stopping hotkey listener: {e}")
            
            # Stop bot if running
            if self.bot_running:
                self.stop_bot()
                
            # Save settings
            self.save_settings()
            
            # Close application
            self.root.quit()
            
        except Exception as e:
            print(f"Error during close: {e}")
            self.root.quit()
            
    def validate_numeric_field(self, field_name, value, min_val=0, max_val=100):
        """Validate numeric input fields"""
        try:
            num_val = int(value)
            if min_val <= num_val <= max_val:
                return True
            else:
                print(f"{field_name} must be between {min_val} and {max_val}")
                return False
        except ValueError:
            print(f"{field_name} must be a number")
            return False

def main():
    root = tk.Tk()
    TrainingAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()
