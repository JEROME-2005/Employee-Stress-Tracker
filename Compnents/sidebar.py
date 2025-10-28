"""
components/sidebar.py - Reusable Sidebar Component
Navigation sidebar used across all pages.
"""

import tkinter as tk
from config import COLORS


def create_sidebar(app, parent, is_admin=False):
    """Create and return the sidebar frame."""
    sidebar = tk.Frame(parent, bg=COLORS['bg_darker'], width=280)
    sidebar.pack(side='left', fill='y')
    sidebar.pack_propagate(False)
    
    # Logo
    logo_frame = tk.Frame(sidebar, bg=COLORS['bg_darker'])
    logo_frame.pack(pady=30, padx=20)
    tk.Label(logo_frame, text="🏠 Stress Monitor", font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg_darker'], fg=COLORS['text_primary'], anchor='w').pack()
    
    # Navigation
    nav_frame = tk.Frame(sidebar, bg=COLORS['bg_darker'])
    nav_frame.pack(fill='both', expand=True, padx=15, pady=20)
    
    buttons = [
        ("🏠  Dashboard", lambda: show_dashboard(app, is_admin)),
    ]
    
    if not is_admin:
        buttons.append(("🎵  Playlist", lambda: show_playlist(app)))
    
    buttons.append(("👤  Profile", lambda: show_profile(app, is_admin)))
    
    if is_admin:
        buttons.append(("👥  Admin", lambda: show_admin_panel(app)))
    
    for text, cmd in buttons:
        btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 11),
                      bg=COLORS['bg_card'], fg=COLORS['text_primary'],
                      relief='flat', anchor='w', padx=15, pady=12, cursor='hand2', bd=0,
                      command=cmd)
        btn.pack(fill='x', pady=3)
    
    # Logout
    logout_frame = tk.Frame(sidebar, bg=COLORS['bg_darker'])
    logout_frame.pack(side='bottom', fill='x', padx=15, pady=20)
    tk.Button(logout_frame, text="👤  Log out", font=('Segoe UI', 11),
             bg=COLORS['bg_card'], fg=COLORS['text_secondary'],
             relief='flat', anchor='w', padx=15, pady=12, cursor='hand2', bd=0,
             command=lambda: show_login(app)).pack(fill='x')
    tk.Label(logout_frame, text="Stress Monitor v1.0", font=('Segoe UI', 8),
            bg=COLORS['bg_darker'], fg=COLORS['text_secondary']).pack(pady=15)


def show_login(app):
    """Navigate to login page."""
    from pages.login_page import show_login as login_page
    login_page(app)


def show_dashboard(app, is_admin):
    """Navigate to appropriate dashboard."""
    if is_admin:
        from pages.admin_dashboard_page import show_admin_dashboard
        show_admin_dashboard(app)
    else:
        from pages.user_dashboard_page import show_user_dashboard
        show_user_dashboard(app)


def show_playlist(app):
    """Navigate to playlist page."""
    from pages.playlist_page import show_playlist as playlist_page
    playlist_page(app)


def show_profile(app, is_admin):
    """Navigate to profile page."""
    from pages.profile_page import show_profile as profile_page
    profile_page(app, is_admin)


def show_admin_panel(app):
    """Navigate to admin panel."""
    from pages.admin_panel_page import show_admin_panel as admin_panel_page
    admin_panel_page(app)