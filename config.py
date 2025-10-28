"""
config.py - Application Configuration and Constants
Centralized configuration for colors, thresholds, and settings.
"""

# Color Theme
COLORS = {
    'bg_dark': '#1e293b',
    'bg_darker': '#0f172a',
    'bg_card': '#293548',
    'bg_input': '#374557',
    'text_primary': '#ffffff',
    'text_secondary': '#94a3b8',
    'accent_blue': '#3b82f6',
    'accent_green': '#22c55e',
    'accent_red': '#ef4444',
    'accent_purple': '#7c3aed',
    'border': '#475569'
}

# Eye Detection Settings
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 3

# Calibration Settings
CALIBRATION_DURATION = 10  # seconds

# Stress Detection Settings
STRESS_ALERT_THRESHOLD = 0.9  # 90%
FPS = 32

# Window Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Stress Monitor v1.0"

# Activity Timeout
ACTIVITY_TIMEOUT = 5  # seconds

# Report Settings
REPORTS_FOLDER = "reports"
LOG_FILE = "blink_log.txt"