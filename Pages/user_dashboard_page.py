"""
pages/user_dashboard_page.py - User Dashboard Page
Main monitoring page with live camera feed and stress metrics.
"""

import tkinter as tk
from config import COLORS
from components.sidebar import create_sidebar


def show_user_dashboard(app):
    """Display the user dashboard."""
    app.clear_window()
    
    container = tk.Frame(app.root, bg=COLORS['bg_dark'])
    container.pack(fill='both', expand=True)
    
    create_sidebar(app, container, is_admin=False)
    
    main = tk.Frame(container, bg=COLORS['bg_dark'])
    main.pack(side='left', fill='both', expand=True)
    
    # Header
    header = tk.Frame(main, bg=COLORS['bg_dark'])
    header.pack(fill='x', padx=40, pady=30)
    tk.Label(header, text="Dashboard", font=('Segoe UI', 32, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(side='left')
    
    # Main Content
    content = tk.Frame(main, bg=COLORS['bg_dark'])
    content.pack(fill='both', expand=True, padx=40, pady=20)
    
    grid = tk.Frame(content, bg=COLORS['bg_dark'])
    grid.pack(fill='both', expand=True)
    
    # Left: Video Feed
    left = tk.Frame(grid, bg=COLORS['bg_dark'])
    left.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    video_card = tk.Frame(left, bg=COLORS['bg_card'], 
                         highlightbackground=COLORS['border'], highlightthickness=1)
    video_card.pack(fill='both', expand=True)
    
    tk.Label(video_card, text="Live Camera Feed", font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['text_primary']).pack(pady=15, padx=20, anchor='w')
    
    video_frame = tk.Frame(video_card, bg=COLORS['bg_darker'], height=400)
    video_frame.pack(fill='both', expand=True, padx=15, pady=(0, 0))
    
    app.video_label = tk.Label(video_frame, bg=COLORS['bg_darker'], text="Camera Feed",
                                font=('Segoe UI', 14), fg=COLORS['text_secondary'])
    app.video_label.pack(fill='both', expand=True)
    
    btn_frame = tk.Frame(video_card, bg=COLORS['bg_card'])
    btn_frame.pack(pady=15, padx=15)
    
    app.monitor_btn = tk.Button(btn_frame, text="Start Monitoring",
                                 font=('Segoe UI', 11, 'bold'), bg=COLORS['accent_green'],
                                 fg=COLORS['text_primary'], relief='flat', padx=25, pady=11,
                                 cursor='hand2', bd=0, command=app.toggle_monitoring)
    app.monitor_btn.pack(side='left', padx=5)
    
    # Right: Metrics Panel
    right = tk.Frame(grid, bg=COLORS['bg_dark'], width=320)
    right.pack(side='left', fill='y')
    right.pack_propagate(False)
    
    # FPS Card
    fps_card = tk.Frame(right, bg=COLORS['accent_blue'], 
                       highlightbackground=COLORS['border'], highlightthickness=1)
    fps_card.pack(fill='x', pady=(0, 12))
    fps_content = tk.Frame(fps_card, bg=COLORS['accent_blue'])
    fps_content.pack(pady=15, padx=15, fill='x')
    tk.Label(fps_content, text="FPS", font=('Segoe UI', 20), bg=COLORS['accent_blue']).pack(side='left', padx=(0, 12))
    fps_info = tk.Frame(fps_content, bg=COLORS['accent_blue'])
    fps_info.pack(side='left')
    tk.Label(fps_info, text="FPS", font=('Segoe UI', 9), bg=COLORS['accent_blue'], fg='white').pack(anchor='w')
    app.fps_label = tk.Label(fps_info, text="32", font=('Segoe UI', 20, 'bold'), 
                            bg=COLORS['accent_blue'], fg='white')
    app.fps_label.pack(anchor='w')
    
    # Eye Detection Card
    detect_card = tk.Frame(right, bg=COLORS['accent_purple'], 
                          highlightbackground=COLORS['border'], highlightthickness=1)
    detect_card.pack(fill='x', pady=(0, 12))
    detect_content = tk.Frame(detect_card, bg=COLORS['accent_purple'])
    detect_content.pack(pady=15, padx=15, fill='x')
    tk.Label(detect_content, text="EYE", font=('Segoe UI', 20), bg=COLORS['accent_purple']).pack(side='left', padx=(0, 12))
    detect_info = tk.Frame(detect_content, bg=COLORS['accent_purple'])
    detect_info.pack(side='left')
    tk.Label(detect_info, text="Detection + Emotion", font=('Segoe UI', 9), bg=COLORS['accent_purple'], fg='white').pack(anchor='w')
    app.blink_label = tk.Label(detect_info, text="0 Blinks", font=('Segoe UI', 14, 'bold'), 
                              bg=COLORS['accent_purple'], fg='white')
    app.blink_label.pack(anchor='w')
    app.emotion_label = tk.Label(detect_info, text="Neutral", font=('Segoe UI', 12), 
                                bg=COLORS['accent_purple'], fg='#c4b5fd')
    app.emotion_label.pack(anchor='w')
    
    # Stress Score Card
    time_card = tk.Frame(right, bg=COLORS['accent_green'], 
                        highlightbackground=COLORS['border'], highlightthickness=1)
    time_card.pack(fill='x')
    time_content = tk.Frame(time_card, bg=COLORS['accent_green'])
    time_content.pack(pady=15, padx=15, fill='x')
    tk.Label(time_content, text="TIME", font=('Segoe UI', 20), bg=COLORS['accent_green']).pack(side='left', padx=(0, 12))
    time_info = tk.Frame(time_content, bg=COLORS['accent_green'])
    time_info.pack(side='left')
    tk.Label(time_info, text="Stress Score", font=('Segoe UI', 9), bg=COLORS['accent_green'], fg='white').pack(anchor='w')
    app.stress_events_label = tk.Label(time_info, text="0% Stress", font=('Segoe UI', 14, 'bold'), 
                                      bg=COLORS['accent_green'], fg='white')
    app.stress_events_label.pack(anchor='w')
    tk.Label(time_info, text="Real-time", font=('Segoe UI', 11), bg=COLORS['accent_green'], fg='#86efac').pack(anchor='w')