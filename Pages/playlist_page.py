"""
pages/playlist_page.py - Calming Playlist Page
Displays curated Spotify playlists for stress relief.
"""

import tkinter as tk
import webbrowser
from config import COLORS
from components.sidebar import create_sidebar


def show_playlist(app):
    """Display the calming playlist page."""
    app.clear_window()
    
    container = tk.Frame(app.root, bg=COLORS['bg_dark'])
    container.pack(fill='both', expand=True)
    
    create_sidebar(app, container, is_admin=False)
    
    main = tk.Frame(container, bg=COLORS['bg_dark'])
    main.pack(side='left', fill='both', expand=True)
    
    # Header
    header = tk.Frame(main, bg=COLORS['bg_dark'])
    header.pack(fill='x', padx=40, pady=30)
    tk.Label(header, text="Calming Playlist", font=('Segoe UI', 32, 'bold'),
            bg=COLORS['bg_dark'], fg=COLORS['text_primary']).pack(side='left')
    
    # Content
    content = tk.Frame(main, bg=COLORS['bg_dark'])
    content.pack(fill='both', expand=True, padx=40, pady=20)
    
    tk.Label(content, text="Calming music can help reduce stress levels",
            font=('Segoe UI', 14),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']).pack(pady=(0, 20))
    
    playlists = [
        ("Peaceful Piano", "37i9dQZF1DXZZbwlv3Vmtr"),
        ("Calming Acoustic", "37i9dQZF1DXaImRpG7HXqp"),
        ("Peaceful Meditation", "37i9dQZF1DWXe9gFZP0gtP"),
        ("Nature Sounds", "37i9dQZF1DX4PP3DA4J0N8")
    ]
    
    playlist_frame = tk.Frame(content, bg=COLORS['bg_card'], padx=20, pady=20)
    playlist_frame.pack(fill='both', expand=True)
    
    def open_spotify_playlist(playlist_id):
        """Open Spotify playlist in browser."""
        webbrowser.open(f"https://open.spotify.com/playlist/{playlist_id}")
    
    for title, playlist_id in playlists:
        btn = tk.Button(playlist_frame,
                      text=title,
                      font=('Segoe UI', 12),
                      bg=COLORS['bg_input'],
                      fg=COLORS['text_primary'],
                      relief='flat',
                      padx=20,
                      pady=15,
                      cursor='hand2',
                      command=lambda pid=playlist_id: open_spotify_playlist(pid))
        btn.pack(fill='x', pady=10)
    
    tk.Label(playlist_frame,
            text="Click on any playlist to open it in your browser",
            font=('Segoe UI', 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']).pack(pady=(20, 0))