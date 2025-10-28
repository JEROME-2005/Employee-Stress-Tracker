"""
components/avatar.py - Reusable Avatar Component
Creates customizable user avatars with optional admin badge.
"""

import tkinter as tk


def create_avatar_with_badge(parent, is_admin=False):
    """Create and return an avatar container with optional admin badge."""
    avatar_container = tk.Frame(parent, bg=parent['bg'])
    avatar_container.pack(pady=30)
    
    avatar = tk.Canvas(avatar_container, width=120, height=120,
                      bg=parent['bg'], highlightthickness=0)
    avatar.pack()
    
    # Head
    avatar.create_oval(30, 10, 90, 70, fill='#60a5fa', outline='')
    
    # Body
    avatar.create_arc(20, 50, 100, 130, start=0, extent=180,
                     fill='#3b82f6', outline='')
    
    # Admin Badge
    if is_admin:
        badge_x, badge_y = 85, 85
        avatar.create_oval(badge_x-18, badge_y-18, badge_x+18, badge_y+18,
                         fill='#1e293b', outline='')
        avatar.create_oval(badge_x-15, badge_y-15, badge_x+15, badge_y+15,
                         fill='#60a5fa', outline='')
        avatar.create_polygon(badge_x, badge_y-8, badge_x-6, badge_y-2,
                            badge_x-6, badge_y+4, badge_x, badge_y+8,
                            badge_x+6, badge_y+4, badge_x+6, badge_y-2,
                            fill='#1e40af', outline='')
    
    return avatar_container