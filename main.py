"""
main.py - Main Application Entry Point
This is the entry point for the Stress Monitor application.
It imports and initializes all components.
"""

import tkinter as tk
from app import StressMonitorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = StressMonitorApp(root)
    root.mainloop()